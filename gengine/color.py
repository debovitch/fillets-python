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
Color class for convenient color handling.
"""

import pygame

class Color:
    """Simple color class that matches the C++ implementation."""
    
    def __init__(self, r=0, g=0, b=0, a=255):
        """
        Initialize a color.
        
        Args:
            r (int): Red component (0-255)
            g (int): Green component (0-255)
            b (int): Blue component (0-255)
            a (int): Alpha component (0-255), defaults to 255 (fully opaque)
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    def get_r(self):
        """Get red component."""
        return self.r
    
    def get_g(self):
        """Get green component."""
        return self.g
    
    def get_b(self):
        """Get blue component."""
        return self.b
    
    def get_a(self):
        """Get alpha component."""
        return self.a
    
    def set_r(self, r):
        """Set red component."""
        self.r = r
    
    def set_g(self, g):
        """Set green component."""
        self.g = g
    
    def set_b(self, b):
        """Set blue component."""
        self.b = b
    
    def set_a(self, a):
        """Set alpha component."""
        self.a = a
    
    def to_tuple(self):
        """
        Convert to a tuple representation.
        
        Returns:
            tuple: (r, g, b, a)
        """
        return (self.r, self.g, self.b, self.a)
    
    def to_pygame_color(self):
        """
        Convert to a pygame.Color.
        
        Returns:
            pygame.Color: The pygame color
        """
        return pygame.Color(self.r, self.g, self.b, self.a)