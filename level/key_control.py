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

class KeyControl:
    """
    Keyboard controls for game movement.
    Maps keyboard keys to movement directions.
    """
    
    def __init__(self):
        """
        Initialize keyboard controls with default arrow keys.
        """
        self.up = pygame.K_UP
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
    
    def set_up(self, key):
        """
        Set the key for moving up.
        
        Args:
            key: The key code
        """
        self.up = key
    
    def set_down(self, key):
        """
        Set the key for moving down.
        
        Args:
            key: The key code
        """
        self.down = key
    
    def set_left(self, key):
        """
        Set the key for moving left.
        
        Args:
            key: The key code
        """
        self.left = key
    
    def set_right(self, key):
        """
        Set the key for moving right.
        
        Args:
            key: The key code
        """
        self.right = key
    
    def get_up(self):
        """
        Get the key for moving up.
        
        Returns:
            The key code for moving up
        """
        return self.up
    
    def get_down(self):
        """
        Get the key for moving down.
        
        Returns:
            The key code for moving down
        """
        return self.down
    
    def get_left(self):
        """
        Get the key for moving left.
        
        Returns:
            The key code for moving left
        """
        return self.left
    
    def get_right(self):
        """
        Get the key for moving right.
        
        Returns:
            The key code for moving right
        """
        return self.right