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

import os
import sys
import pygame
from gengine.agent.sound_agent import SoundAgent
from gengine.log import log_warning
from gengine.ex_info import ExInfo

class PygameSoundAgent(SoundAgent):
    """
    Sound agent implementation using Pygame's mixer.
    """
    
    def __init__(self):
        """
        Initialize the Pygame sound agent.
        """
        super().__init__()
        self.music = None
        self.playing_path = ""
        self.sound_volume = self.MAX_VOLUME
        self.music_volume = self.MAX_VOLUME
        self.finished_callback = None
        self.sound_cache = {}  # Cache of loaded sounds
    
    def own_init(self):
        """
        Initialize the sound system.
        """
        # Call parent init to set up watchers
        super().own_init()
        
        try:
            # Initialize Pygame mixer
            pygame.mixer.init(44100, -16, 2, 1024)
            
            # Set up music end event
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            
        except pygame.error as e:
            sys.exit(ExInfo("Could not initialize sound system").add_info("error", str(e)))
    
    def own_shutdown(self):
        """
        Shut down the sound system.
        """
        self.stop_music()
        pygame.mixer.quit()
    
    def reinit(self):
        """
        Reinitialize the sound system.
        """
        super().reinit()
        self.music = None
        self.sound_volume = self.MAX_VOLUME
        self.music_volume = self.MAX_VOLUME
    
    def set_sound_volume(self, volume):
        """
        Set the sound effects volume.
        
        Args:
            volume (int): Volume level (0-100)
        """
        # Convert 0-100 to 0-1.0 (Pygame's volume range)
        self.sound_volume = min(self.MAX_VOLUME, max(0, volume)) / 100.0 * self.MAX_VOLUME
        # This will affect new sounds, but not already playing ones
    
    def set_music_volume(self, volume):
        """
        Set the music volume.
        
        Args:
            volume (int): Volume level (0-100)
        """
        # Convert 0-100 to 0-1.0 (Pygame's volume range)
        self.music_volume = min(self.MAX_VOLUME, max(0, volume)) / 100.0 * self.MAX_VOLUME
        pygame.mixer.music.set_volume(self.music_volume / self.MAX_VOLUME)
    
    def generate_id_name(self, file_path):
        """
        Generate a unique ID for a sound file.
        
        Args:
            file_path: Path to the sound file
            
        Returns:
            str: A unique ID for the sound
        """
        path_str = file_path
        if hasattr(file_path, 'get_native'):
            path_str = file_path.get_native()
        return os.path.basename(path_str)
    
    def find_chunk(self, name):
        """
        Find a sound chunk in the cache.
        
        Args:
            name (str): The name of the sound
            
        Returns:
            pygame.mixer.Sound: The sound or None if not found
        """
        return self.sound_cache.get(name)

    def find_free_channel(self):
        """
        Find a free mixer channel and return its index and object.

        Returns:
            tuple[int, pygame.mixer.Channel | None]: Channel index and channel.
        """
        for channel_id in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(channel_id)
            if not channel.get_busy():
                return channel_id, channel
        return -1, None
    
    def play_sound(self, sound, volume, loops=0):
        """
        Play a sound effect.
        
        Args:
            sound: Either a Sound object or a path to a sound file
            volume (int): Volume level for this sound (0-100)
            loops (int): Number of times to repeat the sound
        
        Returns:
            int: Channel number or -1 if no free channels
        """
        if not pygame.mixer.get_init():
            return -1

        if volume is None:
            volume = 100
        if loops is None:
            loops = 0
        
        # Convert volume from 0-100 to 0-1.0
        sound_volume = min(100, max(0, volume)) / 100.0
        
        if not sound:
            return -1

        # Get the actual sound object
        sound_obj = sound
        if isinstance(sound, str) or hasattr(sound, 'get_native'):
            # It's a path, load it
            sound_path = sound.get_native() if hasattr(sound, 'get_native') else sound
            sound_id = self.generate_id_name(sound_path)
            sound_obj = self.find_chunk(sound_id)
            if not sound_obj:
                try:
                    sound_obj = pygame.mixer.Sound(sound_path)
                    self.sound_cache[sound_id] = sound_obj
                except pygame.error as e:
                    log_warning(ExInfo("Could not load sound").add_info("file", sound_path).add_info("error", str(e)))
                    return -1
        
        # Apply the base sound volume and specific volume for this sound
        sound_obj.set_volume(sound_volume * (self.sound_volume / self.MAX_VOLUME))
        
        # Play the sound
        try:
            channel_id, channel = self.find_free_channel()
            if channel is None:
                log_warning(ExInfo("Could not play sound").add_info("error", "no free channel"))
                return -1

            channel.play(sound_obj, loops=loops)
            return channel_id
        except pygame.error as e:
            log_warning(ExInfo("Could not play sound").add_info("error", str(e)))
            return -1
    
    def play_music(self, file_path, finished_msg=None):
        """
        Play music from a file.
        
        Args:
            file_path: Path to the music file
            finished_msg: Message to send when music finishes playing
        """
        if not pygame.mixer.get_init():
            # No sound system, just discard the message
            if finished_msg:
                del finished_msg
            return
        
        # Stop any currently playing music
        self.stop_music()
        
        # Store the callback message
        self.finished_callback = finished_msg
        
        # Get the file path as a string
        path_str = file_path
        if hasattr(file_path, 'get_native'):
            path_str = file_path.get_native()
        
        # Try to load and play the music
        try:
            pygame.mixer.music.load(path_str)
            pygame.mixer.music.set_volume(self.music_volume / self.MAX_VOLUME)
            pygame.mixer.music.play()
            self.playing_path = path_str
            # log_debug(ExInfo("Playing music").add_info("file", path_str))
        except pygame.error as e:
            log_warning(ExInfo("Could not play music").add_info("file", path_str).add_info("error", str(e)))
            # Discard the message since we couldn't play the music
            if finished_msg:
                del finished_msg
                self.finished_callback = None
    
    def stop_music(self):
        """
        Stop currently playing music.
        """
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        # Discard the callback message
        if self.finished_callback:
            del self.finished_callback
            self.finished_callback = None
        
        self.playing_path = ""
    
    def handle_music_end_event(self):
        """
        Handle the music end event.
        This should be called when a USEREVENT is received.
        """
        if self.finished_callback and not pygame.mixer.music.get_busy():
            # Send the finished message
            self.finished_callback.send_clone()
            self.finished_callback = None
