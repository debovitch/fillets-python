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
from gengine.v2 import V2

class MouseStroke:
    """
    Contains information about a mouse click.
    """
    
    def __init__(self, event, x=None, y=None):
        """
        Create a new mouse stroke from either a pygame event or button/position values.
        
        Args:
            event: Either a pygame event or the button number
            x: X position (only used if event is a button number)
            y: Y position (only used if event is a button number)
        """
        if x is not None and y is not None:
            # Called with (button, x, y)
            self.button = event
            self.loc = V2(x, y)
        else:
            # Called with a pygame event
            self.button = event.button
            self.loc = V2(event.pos[0], event.pos[1])
    
    def is_left(self):
        """
        Check if this is a left mouse button click.
        
        Returns:
            bool: True if it's a left mouse button click
        """
        return self.button == 1  # pygame.BUTTON_LEFT = 1
    
    def is_middle(self):
        """
        Check if this is a middle mouse button click.
        
        Returns:
            bool: True if it's a middle mouse button click
        """
        return self.button == 2  # pygame.BUTTON_MIDDLE = 2
    
    def is_right(self):
        """
        Check if this is a right mouse button click.
        
        Returns:
            bool: True if it's a right mouse button click
        """
        return self.button == 3  # pygame.BUTTON_RIGHT = 3
        
    def is_button(self):
        """
        Check if this is a button event.
        
        Returns:
            bool: True if this is a button event
        """
        return self.button > 0
    
    def get_loc(self):
        """
        Get the location of the mouse click.
        
        Returns:
            V2: The location of the mouse click
        """
        return self.loc
    
    def to_string(self):
        """
        Get a string representation of this mouse stroke.
        
        Returns:
            str: A string representation
        """
        return str(self.button)
    
    def __str__(self):
        """
        Get a string representation of this mouse stroke.
        
        Returns:
            str: A string representation
        """
        return self.to_string()