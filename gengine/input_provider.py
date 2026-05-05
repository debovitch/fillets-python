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

from abc import ABC, abstractmethod

class InputProvider(ABC):
    """
    Interface to pressed keys and mouse location.
    """
    
    @abstractmethod
    def is_pressed(self, key):
        """
        Check if a key is pressed.
        
        Args:
            key (int): The key code
            
        Returns:
            bool: True if the key is pressed
        """
        pass
    
    @abstractmethod
    def is_left_pressed(self):
        """
        Check if the left mouse button is pressed.
        
        Returns:
            bool: True if the left mouse button is pressed
        """
        pass
    
    @abstractmethod
    def is_middle_pressed(self):
        """
        Check if the middle mouse button is pressed.
        
        Returns:
            bool: True if the middle mouse button is pressed
        """
        pass
    
    @abstractmethod
    def is_right_pressed(self):
        """
        Check if the right mouse button is pressed.
        
        Returns:
            bool: True if the right mouse button is pressed
        """
        pass
    
    @abstractmethod
    def get_mouse_loc(self):
        """
        Get the mouse location.
        
        Returns:
            V2: The mouse location
        """
        pass
    
    @abstractmethod
    def to_string(self):
        """
        Get a string representation of the input state.
        
        Returns:
            str: A string representation
        """
        pass