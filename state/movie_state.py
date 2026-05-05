#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of Fillets Python.
#
# Fillets Python is a Python port of the game Fish Fillets NG.
# Original project: https://github.com/FishFilletsNG
#                   https://fillets.sourceforge.net/
#
# Copyright (C) 2026 Thierry Duchassin
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <https://www.gnu.org/licenses/>.
#
# This file is an independent Python reimplementation and not part of
# the original Fish Fillets NG codebase.

"""
MPEG movie playback state.
"""

import pygame

from gengine.agent.option_agent import OptionAgent
from gengine.agent.sound_agent import SoundAgent
from gengine.agent.timer_agent import TimerAgent
from gengine.agent.video_agent import VideoAgent
from gengine.ex_info import ExInfo
from gengine.log import log_warning
from plan.game_state import GameState
from state.demo_input import DemoInput


class MovieState(GameState):
    """
    Play a MPEG movie with PyAV-decoded video frames and pygame audio.
    """

    def __init__(self, file_path):
        """
        Initialize a movie state.

        Args:
            file_path: Path to the movie file
        """
        GameState.__init__(self)
        self.file = file_path
        self.container = None
        self.video_stream = None
        self.frames = None
        self.current_frame = None
        self.next_frame = None
        self.first_frame_time = 0.0
        self.started_at = 0
        self.video_ended = False
        self.audio_sound = None
        self.audio_channel = None
        self.old_timer_interval = None
        self.take_handler(DemoInput(self))

    @staticmethod
    def is_available():
        """Return True when the PyAV backend is importable."""
        try:
            import av  # noqa: F401
            return True
        except ImportError:
            return False

    def get_name(self):
        """
        Get the state name.

        Returns:
            str: The state name
        """
        return "state_movie"

    def own_init_state(self):
        """Open the movie, resize the window and start playback."""
        try:
            import av

            SoundAgent.agent().stop_music()

            self.container = av.open(self.file.get_native())
            self.video_stream = self._find_stream(self.container.streams, "video")
            if self.video_stream is None:
                raise RuntimeError("movie has no video stream")

            self._init_video_mode()
            self._init_movie_timer()

            self.frames = self.container.decode(self.video_stream)
            first_frame = self._read_next_frame()
            if first_frame is None:
                raise RuntimeError("movie has no decodable video frame")

            self.first_frame_time = self._frame_time(first_frame)
            self.current_frame = self._surface_from_frame(first_frame)
            self.next_frame = self._read_next_frame()

            self.audio_sound = self._load_audio()
            if self.audio_sound:
                self.audio_channel = self.audio_sound.play()

            self.started_at = pygame.time.get_ticks()
        except Exception as exc:
            log_warning(ExInfo("cannot play movie")
                        .add_info("file", self.file.get_native())
                        .add_info("error", str(exc)))
            self._cleanup_movie()
            self.quit_state()

    def own_update_state(self):
        """Advance video frames and quit when playback is done."""
        if not self.container:
            self.quit_state()
            return

        movie_time = self.first_frame_time + (
            (pygame.time.get_ticks() - self.started_at) / 1000.0
        )

        frame_to_show = None
        while self.next_frame is not None and self._frame_time(self.next_frame) <= movie_time:
            frame_to_show = self.next_frame
            self.next_frame = self._read_next_frame()

        if frame_to_show is not None:
            self.current_frame = self._surface_from_frame(frame_to_show)

        if self.video_ended:
            if self.audio_channel is None or not self.audio_channel.get_busy():
                self.quit_state()

    def own_pause_state(self):
        """Pause movie audio."""
        if self.audio_channel:
            self.audio_channel.pause()

    def own_resume_state(self):
        """Resume movie audio."""
        if self.audio_channel:
            self.audio_channel.unpause()

    def own_clean_state(self):
        """Release movie resources and restore normal game sound timing."""
        self._cleanup_movie()
        SoundAgent.agent().reinit()

    def draw_on(self, screen):
        """
        Draw the current movie frame.

        Args:
            screen: Pygame screen surface
        """
        if self.current_frame:
            screen.blit(self.current_frame, (0, 0))

    def _init_video_mode(self):
        """Resize the pygame window to the movie dimensions."""
        options = OptionAgent.agent()
        options.set_param("screen_width", self.video_stream.width)
        options.set_param("screen_height", self.video_stream.height)
        VideoAgent.agent().init_video_mode()

    def _init_movie_timer(self):
        """Use a timer interval close to the movie frame rate."""
        fps = self.video_stream.average_rate
        if fps:
            timer = TimerAgent.agent()
            self.old_timer_interval = timer.time_interval
            timer.time_interval = max(1, int(1000 / float(fps)))

    def _read_next_frame(self):
        """Read the next decoded video frame."""
        try:
            return next(self.frames)
        except StopIteration:
            self.video_ended = True
            return None

    def _surface_from_frame(self, frame):
        """Convert a PyAV frame into a pygame surface."""
        array = frame.to_ndarray(format="rgb24")
        height, width = array.shape[:2]
        return pygame.image.frombuffer(array.tobytes(), (width, height), "RGB").convert()

    def _load_audio(self):
        """Decode the movie audio stream into a pygame Sound."""
        if not OptionAgent.agent().get_as_bool("sound", True):
            return None
        if not pygame.mixer.get_init():
            return None

        audio_container = None
        try:
            import av
            from av.audio.resampler import AudioResampler

            audio_container = av.open(self.file.get_native())
            audio_stream = self._find_stream(audio_container.streams, "audio")
            if audio_stream is None:
                return None

            frequency, _, channels = pygame.mixer.get_init()
            layout = "stereo" if channels == 2 else "mono"
            resampler = AudioResampler(format="s16", layout=layout, rate=frequency)
            pcm = bytearray()

            for frame in audio_container.decode(audio_stream):
                self._append_audio_frames(pcm, resampler.resample(frame))

            self._append_audio_frames(pcm, resampler.resample(None))
            if not pcm:
                return None

            sound = pygame.mixer.Sound(buffer=bytes(pcm))
            sound.set_volume(self._movie_volume())
            return sound
        except Exception as exc:
            log_warning(ExInfo("cannot decode movie audio")
                        .add_info("file", self.file.get_native())
                        .add_info("error", str(exc)))
            return None
        finally:
            if audio_container is not None:
                audio_container.close()

    def _append_audio_frames(self, pcm, frames):
        """Append packed signed 16-bit audio frames to pcm."""
        if not frames:
            return

        for frame in frames:
            pcm.extend(frame.to_ndarray().tobytes())

    def _movie_volume(self):
        """Return the intro audio volume as a pygame 0.0-1.0 value."""
        volume = OptionAgent.agent().get_as_int("volume_music", 50)
        return min(100, max(0, volume)) / 100.0

    def _cleanup_movie(self):
        """Stop playback and close opened resources."""
        if self.audio_channel:
            self.audio_channel.stop()
            self.audio_channel = None

        self.audio_sound = None
        self.current_frame = None
        self.next_frame = None
        self.frames = None

        if self.container is not None:
            self.container.close()
            self.container = None

        if self.old_timer_interval is not None:
            TimerAgent.agent().time_interval = self.old_timer_interval
            self.old_timer_interval = None

    @staticmethod
    def _find_stream(streams, stream_type):
        """Find the first stream of a given type."""
        for stream in streams:
            if stream.type == stream_type:
                return stream
        return None

    @staticmethod
    def _frame_time(frame):
        """Return a frame timestamp in seconds."""
        if frame.time is not None:
            return float(frame.time)
        return 0.0
