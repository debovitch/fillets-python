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

from enum import Enum, auto
import pygame

from gengine.no_copy import NoCopy
from gengine.path import Path
from gengine.agent.option_agent import OptionAgent
from gengine.agent.sound_agent import SoundAgent
from gengine.resource.res_dialog_pack import ResDialogPack
from gengine.agent.timer_agent import TimerAgent

class DialogPair:
    """
    Pair of dialog parts - picture and subtitle text.
    """
    
    def __init__(self, picture_file=None, subtitle=""):
        """
        Initialize a new dialog pair.
        
        Args:
            picture_file: Path to the picture file
            subtitle: Subtitle text
        """
        self.picture_file = picture_file
        self.subtitle = subtitle
    
    def is_empty(self):
        """
        Check if this pair is empty.
        
        Returns:
            bool: True if this pair is empty
        """
        return not self.picture_file and not self.subtitle
    
    def get_picture_file(self):
        """
        Get the picture file.
        
        Returns:
            Path: The picture file
        """
        return self.picture_file
    
    def get_subtitle(self):
        """
        Get the subtitle.
        
        Returns:
            str: The subtitle
        """
        return self.subtitle

class DialogMode(Enum):
    """Dialog mode enum."""
    NORMAL = auto()
    LEFT = auto()
    RIGHT = auto()


class PlannedDialog:
    """Active dialog sound/minimum subtitle lifetime."""

    def __init__(self, actor, channel_id, min_cycles, loops):
        self.actor = actor
        self.channel_id = channel_id
        if loops == -1:
            self.end_cycle = 1 << 30
        else:
            self.end_cycle = (
                TimerAgent.agent().get_cycles() + min_cycles * (loops + 1)
            )

    def equals_actor(self, actor):
        return self.actor == actor

    def is_playing(self):
        if self.channel_id < 0 or not pygame.mixer.get_init():
            return False
        return pygame.mixer.Channel(self.channel_id).get_busy()

    def is_talking(self):
        if self.channel_id > -1:
            return self.is_playing()
        return self.end_cycle > TimerAgent.agent().get_cycles()

    def kill_talk(self):
        if self.is_playing():
            pygame.mixer.Channel(self.channel_id).stop()


class FishDialog(NoCopy):
    """
    Dialog planner for fish.
    Handles dialog display and sound playback.
    """
    
    def __init__(self):
        """Initialize a new fish dialog."""
        self.dialogs = []
        self.running = []
        self.cycling = []
        self.active_dialog = None
        self.dialog_pack = ResDialogPack()
        self.talking = set()
        self.model_dialogs = {}
        self.model_sounds = {}
        self.mode = DialogMode.NORMAL
        self.subagent = None
    
    def set_subtitle_agent(self, agent):
        """
        Set the subtitle agent.
        
        Args:
            agent: The subtitle agent
        """
        self.subagent = agent
    
    def are_running(self):
        """
        Check if dialogs are running.
        
        Returns:
            bool: True if dialogs are running
        """
        return any(dialog.is_talking() for dialog in self.running + self.cycling)

    def update_stack(self):
        """Remove the first completed running dialog."""
        for index, dialog in enumerate(self.running):
            if not dialog.is_talking():
                dialog.kill_talk()
                self.running.pop(index)
                if dialog is self.active_dialog:
                    self.active_dialog = None
                return

    def is_dialog(self):
        """Return true when a blocking dialog is active."""
        return bool(self.active_dialog and self.active_dialog.is_talking())
    
    def is_talking(self, index):
        """
        Check if a model is talking.
        
        Args:
            index: The model index
            
        Returns:
            bool: True if the model is talking
        """
        return any(
            dialog.equals_actor(index) and dialog.is_talking()
            for dialog in self.running + self.cycling
        )
    
    def kill_sound(self, index):
        """
        Kill the sound for a model.
        
        Args:
            index: The model index
        """
        self._kill_sound_in(index, self.running)
        self._kill_sound_in(index, self.cycling)

    def _kill_sound_in(self, index, dialogs):
        for dialog in list(dialogs):
            if dialog.equals_actor(index):
                dialog.kill_talk()
                dialogs.remove(dialog)
                if dialog is self.active_dialog:
                    self.active_dialog = None

    def kill_talks(self):
        """Stop all currently running dialogs."""
        for dialog in self.running + self.cycling:
            dialog.kill_talk()
        self.running.clear()
        self.cycling.clear()
        self.active_dialog = None
        self.dialogs.clear()
        self.talking.clear()
        if self.subagent:
            self.subagent.kill_talks()
    
    def remove_all(self):
        """Remove all dialogs."""
        self.kill_talks()
        self.model_dialogs.clear()
        self.model_sounds.clear()
        self.dialog_pack.remove_all()
            
    def cancel_dialog(self):
        """
        Cancel all current dialogs.
        """
        self.kill_talks()
    
    def run_dialog(self, model_index, dialog_name):
        """
        Run a dialog for a model.
        
        Args:
            model_index: The model index
            dialog_name: The dialog name
            
        Returns:
            bool: True if the dialog was started
        """
        # Already talking?
        if model_index in self.talking:
            return False
        
        # No dialogs for this model?
        if model_index not in self.model_dialogs:
            return False
        
        # Dialog not found?
        model_dict = self.model_dialogs[model_index]
        if dialog_name not in model_dict:
            return False
        
        # Create the dialog
        dialog_pair = model_dict[dialog_name]
        self.dialogs.append(dialog_pair)
        
        # Play dialog sound if available
        self.play_dialog_sound(model_index, dialog_name)
        
        if self.subagent:
            self.subagent.plan_subtitle(dialog_pair, None)
        
        return True
    
    def play_dialog_sound(self, model_index, dialog_name):
        """
        Play a dialog sound.
        
        Args:
            model_index: The model index
            dialog_name: The dialog name
        """
        if model_index not in self.model_sounds:
            return
            
        model_dict = self.model_sounds[model_index]
        if dialog_name not in model_dict:
            return
            
        sound_file = model_dict[dialog_name]
        
        if OptionAgent.agent().get_as_bool("sound", True):
            SoundAgent.agent().play_sound(sound_file, 100)
    
    def add_dialog(self, *args):
        """
        Add a dialog.
        """
        if len(args) == 2:
            name, dialog = args
            self.dialog_pack.add_res(name, dialog)
            return

        model_index, dialog_name, speech_file, subtitle = args

        # Create model entry if it doesn't exist
        if model_index not in self.model_dialogs:
            self.model_dialogs[model_index] = {}
            self.model_sounds[model_index] = {}
        
        speech_path = None
        if speech_file:
            speech_path = Path.data_read_path(speech_file)
        
        # Add dialog and sound
        pair = DialogPair(speech_path, subtitle)
        self.model_dialogs[model_index][dialog_name] = pair
        self.model_sounds[model_index][dialog_name] = speech_path

    def actor_talk(self, model_index, name, volume=75, loops=0, dialog_flag=False):
        """
        Run a localized dialog by name for a model.
        """
        volume = 75 if volume is None else int(volume)
        loops = 0 if loops is None else int(loops)
        dialog_flag = False if dialog_flag is None else bool(dialog_flag)

        args = str(name).split("@")
        dialog_name = args[0]
        subtitle_dialog = self.dialog_pack.find_dialog_hard(dialog_name)
        if not subtitle_dialog:
            return

        subtitle = subtitle_dialog.get_formated_subtitle(args)
        if self.subagent and subtitle:
            self.subagent.new_subtitle(
                subtitle,
                getattr(subtitle_dialog, "fontname", ""),
            )

        speech_dialog = self.dialog_pack.find_dialog_speech(dialog_name) or subtitle_dialog
        channel_id = -1
        if OptionAgent.agent().get_as_bool("sound", True) and not speech_dialog.is_speechless():
            channel_id = SoundAgent.agent().play_sound(
                Path.data_read_path(speech_dialog.soundfile), volume, loops)

        talker = PlannedDialog(
            model_index,
            channel_id,
            subtitle_dialog.get_min_time(),
            loops,
        )
        if loops == -1:
            self.cycling.append(talker)
        else:
            self.running.append(talker)

        if dialog_flag:
            self.active_dialog = talker
    
    def add_dialog_pair(self, small_index, big_index, dialog_name, 
                        speech_small, speech_big, subtitle_small, subtitle_big):
        """
        Add a dialog pair for small and big fish.
        
        Args:
            small_index: The small fish index
            big_index: The big fish index
            dialog_name: The dialog name
            speech_small: The small fish speech file
            speech_big: The big fish speech file
            subtitle_small: The small fish subtitle
            subtitle_big: The big fish subtitle
        """
        # Add small fish dialog
        speech_path_small = None
        if speech_small:
            speech_path_small = Path.data_read_path(speech_small)
        
        self.model_dialogs.setdefault(small_index, {})[dialog_name] = DialogPair(
            speech_path_small, subtitle_small)
        self.model_sounds.setdefault(small_index, {})[dialog_name] = speech_path_small
        
        # Add big fish dialog
        speech_path_big = None
        if speech_big:
            speech_path_big = Path.data_read_path(speech_big)
        
        self.model_dialogs.setdefault(big_index, {})[dialog_name] = DialogPair(
            speech_path_big, subtitle_big)
        self.model_sounds.setdefault(big_index, {})[dialog_name] = speech_path_big
    
    def set_mode(self, mode):
        """
        Set dialog mode.
        
        Args:
            mode: The dialog mode
        """
        self.mode = mode
    
    def get_mode(self):
        """
        Get the dialog mode.
        
        Returns:
            DialogMode: The dialog mode
        """
        return self.mode
    
    def receive_simple(self, msg):
        """
        Handle simple message.
        
        Args:
            msg: The message
        """
        if msg.get_name() == "remove":
            # Remove model from talking set
            model_index = msg.get_param()
            self.talking.discard(model_index)
            
            # Remove first dialog from queue
            if self.dialogs:
                self.dialogs.pop(0)
        else:
            # Unknown message
            pass
