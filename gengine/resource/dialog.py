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
from typing import Optional, List
from gengine.no_copy import NoCopy
from gengine.resource.res_sound_pack import ResSoundPack
from gengine.agent.pygame_sound_agent import PygameSoundAgent

class Dialog(NoCopy):
    """
    Dialog with sound and subtitle.
    Represents a line of dialog with optional sound and text.
    """
    
    DEFAULT_LANG = "en"
    
    def __init__(self, lang: str, soundfile: str, subtitle: str):
        """
        Initialize a new dialog.
        
        Args:
            lang: The language of the dialog
            soundfile: The sound file path (can be empty for speechless dialog)
            subtitle: The subtitle text
        """
        self.sound: Optional[pygame.mixer.Sound] = None
        self.soundfile = soundfile
        self.lang = lang
        self.subtitle = subtitle
    
    def __del__(self):
        """
        Clean up resources when the dialog is deleted.
        """
        # Sound resources are managed by Pygame's garbage collector
        self.sound = None
    
    def is_speechless(self) -> bool:
        """
        Check if this dialog has no sound.
        
        Returns:
            bool: True if the dialog has no sound
        """
        return not self.soundfile
    
    def talk(self, volume: int, loops: int = 0) -> int:
        """
        Play the dialog sound.
        
        Args:
            volume: The volume to play at (0-100)
            loops: Number of times to repeat the sound
            
        Returns:
            int: Channel number or -1 if no free channels
        """
        # If there's no sound file, don't try to play anything
        if self.is_speechless():
            return -1
        
        # Lazy load the sound if it's not already loaded
        if not self.sound and self.soundfile:
            self.sound = ResSoundPack.load_sound(self.soundfile)
        
        # Play the sound
        if self.sound:
            try:
                return PygameSoundAgent.agent().play_sound(self.sound, volume, loops)
            except:
                # If there's an error, return -1
                return -1
        
        return -1
    
    def run_subtitle(self, args: List[str]) -> None:
        """
        Display the subtitle with replaceable arguments.
        In the Python version, this just returns the formatted subtitle
        since the actual display is handled by the SubTitleAgent.
        
        Args:
            args: Arguments to format into the subtitle
        """
        # In the original, this would trigger the subtitle display
        # For now, we'll just ensure the subtitle is formatted
        self.get_formated_subtitle(args)
    
    def get_lang(self) -> str:
        """
        Get the language of this dialog.
        
        Returns:
            str: The language code
        """
        return self.lang
    
    def get_subtitle(self) -> str:
        """
        Get the raw subtitle text.
        
        Returns:
            str: The subtitle text
        """
        return self.subtitle
    
    def get_formated_subtitle(self, args: List[str]) -> str:
        """
        Get the subtitle text with arguments inserted.
        
        Args:
            args: Arguments to format into the subtitle
            
        Returns:
            str: The formatted subtitle
        """
        # Process the subtitle with arguments.
        # In the original, %1, %2, etc. are replaced with args after the name.
        formatted = self.subtitle
        
        for i, arg in enumerate(args[1:], start=1):
            placeholder = f"%{i}"
            formatted = formatted.replace(placeholder, arg)
            
        return formatted
    
    def get_min_time(self) -> int:
        """
        Get the minimum time this dialog should be displayed.
        Based on the length of the subtitle.
        
        Returns:
            int: The minimum time in game cycles
        """
        return min(180, len(self.subtitle))
    
    def equal_sound(self, other) -> bool:
        """
        Check if this dialog uses the same sound as another.
        
        Args:
            other: The other sound to compare with
            
        Returns:
            bool: True if the sounds are the same
        """
        return self.sound == other
