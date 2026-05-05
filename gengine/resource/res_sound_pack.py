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
from typing import Optional
from gengine.resource.resource_pack import ResourcePack
from gengine.ex_info import ExInfo
from gengine.log import log_debug, log_warning
from gengine.agent.option_agent import OptionAgent

class ResSoundPack(ResourcePack[pygame.mixer.Sound]):
    """
    Sound resources.
    Manages loading and unloading of sound resources.
    """
    
    def __init__(self):
        """
        Initialize a new sound pack.
        """
        super().__init__()
    
    def get_name(self) -> str:
        """
        Get the name of this resource pack.
        
        Returns:
            str: The name of the resource pack
        """
        return "sound_pack"
    
    @staticmethod
    def load_sound(file_path) -> Optional[pygame.mixer.Sound]:
        """
        Load unshared sound from file.
        
        Args:
            file_path: The path to the sound file
            
        Returns:
            pygame.mixer.Sound: The loaded sound or None if sound is disabled
        """
        # Check if sound is enabled
        if not OptionAgent.agent().get_as_bool("sound", True):
            return None
        
        # Get the path as a string
        path_str = file_path
        if hasattr(file_path, 'get_native'):
            path_str = file_path.get_native()
        
        try:
            # Initialize the mixer if it's not already initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            # Load the sound
            sound = pygame.mixer.Sound(path_str)
            return sound
        except pygame.error as e:
            log_warning(ExInfo("cannot load sound")
                       .add_info("path", path_str)
                       .add_info("error", str(e)))
            return None
    
    def add_sound(self, name: str, file_path) -> None:
        """
        Store sound under this name.
        Nothing is stored when sound cannot be loaded.
        
        Args:
            name: The name to store the sound under
            file_path: The path to the sound file
        """
        sound = self.load_sound(file_path)
        if sound:
            self.add_res(name, sound)
    
    def unload_res(self, res: pygame.mixer.Sound) -> None:
        """
        Free the given resource.
        
        Args:
            res: The resource to free
        """
        # In Python/Pygame, we don't need to explicitly free sounds
        # They will be garbage collected
        pass