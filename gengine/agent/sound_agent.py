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

import pygame
from gengine.agent.base_agent import BaseAgent, agent_class
from gengine.name import Name
from gengine.agent.option_agent import OptionAgent
from gengine.log import log_debug, log_warning
from gengine.ex_info import ExInfo
from gengine.exceptions import LogicException

@agent_class(Name.SOUND_NAME)
class SoundAgent(BaseAgent):
    """
    Base agent for sound and music playback.
    """
    
    MAX_VOLUME = 128  # 0-128 is Pygame's volume range, equivalent to SDL_mixer's MIX_MAX_VOLUME
    
    def __init__(self):
        """
        Initialize the sound agent.
        """
        super().__init__()
    
    def own_init(self):
        """
        Initialize sound volumes and register parameter watchers.
        """
        self.reinit()
        
        self.register_watcher("volume_sound")
        self.register_watcher("volume_music")
    
    def reinit(self):
        """
        Reinitialize volume settings.
        """
        options = OptionAgent.agent()
        
        # Set default volumes
        options.set_default("volume_sound", 90)
        options.set_default("volume_music", 50)
        
        # Apply volume settings
        self.set_sound_volume(options.get_as_int("volume_sound"))
        self.set_music_volume(options.get_as_int("volume_music"))
    
    def set_sound_volume(self, volume):
        """
        Set the sound effects volume.
        Must be implemented by derived classes.
        
        Args:
            volume (int): Volume level (0-100)
        """
        pass
    
    def set_music_volume(self, volume):
        """
        Set the music volume.
        Must be implemented by derived classes.
        
        Args:
            volume (int): Volume level (0-100)
        """
        pass
    
    def play_sound(self, sound, volume, loops=0):
        """
        Play a sound effect.
        Must be implemented by derived classes.
        
        Args:
            sound: The sound to play
            volume (int): Volume level for this sound (0-100)
            loops (int): Number of times to repeat the sound
        
        Returns:
            int: Channel number or -1 if no free channels
        """
        return -1
    
    def play_music(self, file_path, finished_msg=None):
        """
        Play music from a file.
        Must be implemented by derived classes.
        
        Args:
            file_path: Path to the music file
            finished_msg: Message to send when music finishes playing
        """
        if finished_msg:
            del finished_msg
    
    def stop_music(self):
        """
        Stop currently playing music.
        Must be implemented by derived classes.
        """
        pass
    
    def receive_string(self, msg):
        """
        Handle string messages.
        
        Args:
            msg (StringMsg): The message to handle
        """
        if msg.equals_name("param_changed"):
            param = msg.get_value()
            if param == "volume_sound":
                volume = OptionAgent.agent().get_as_int("volume_sound")
                self.set_sound_volume(volume)
            elif param == "volume_music":
                volume = OptionAgent.agent().get_as_int("volume_music")
                self.set_music_volume(volume)
            else:
                super().receive_string(msg)
        else:
            super().receive_string(msg)