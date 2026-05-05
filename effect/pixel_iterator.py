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
from gengine.no_copy import NoCopy
from gengine.v2 import V2
from effect.surface_lock import SurfaceLock
from effect.pixel_tool import PixelTool

class PixelIterator(NoCopy):
    """
    Iterator over surface pixels.
    Allows efficient traversal of pixels in a surface.
    """
    
    def __init__(self, surface):
        """
        Initialize a new pixel iterator and lock the surface.
        
        Args:
            surface (pygame.Surface): The surface to iterate over
        """
        self.surface = surface
        self.lock = SurfaceLock(surface)
        
        # In Pygame, we'll use a simpler approach with coordinates instead of pointers
        self.x = 0
        self.y = 0
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.position = 0  # Linear position (x + y * width)
        self.total_pixels = self.width * self.height
    
    def __del__(self):
        """
        Clean up resources.
        """
        # The SurfaceLock will be automatically cleaned up by Python
        pass
    
    def set_pos(self, pos):
        """
        Set the current position.
        
        Args:
            pos (V2): The position to set
            
        Raises:
            AssertionError: If the position is outside the surface bounds
        """
        x = pos.get_x()
        y = pos.get_y()
        assert 0 <= x < self.width and 0 <= y < self.height, "Position out of bounds"
        
        self.x = x
        self.y = y
        self.position = y * self.width + x
    
    def is_valid(self):
        """
        Check if the iterator is still valid.
        
        Returns:
            bool: True if the iterator is still within the surface bounds
        """
        return self.position < self.total_pixels
    
    def inc(self):
        """
        Increment the iterator to the next pixel.
        """
        self.position += 1
        self.x += 1
        if self.x >= self.width:
            self.x = 0
            self.y += 1
    
    def is_transparent(self):
        """
        Check if the current pixel is transparent.
        
        Returns:
            bool: True if the pixel is transparent
        """
        # In Pygame, we can check the alpha value directly
        color = self.get_color()
        # Check both colorkey and alpha
        if self.surface.get_flags() & pygame.SRCCOLORKEY:
            # Check if this pixel matches the colorkey
            colorkey = self.surface.get_colorkey()
            pixel_color = self.surface.get_at((self.x, self.y))
            if (pixel_color[0] == colorkey[0] and 
                pixel_color[1] == colorkey[1] and 
                pixel_color[2] == colorkey[2]):
                return True
        
        # Also consider alpha
        return color.a == 0
    
    def get_color(self):
        """
        Get the color at the current position.
        
        Returns:
            pygame.Color: The color at the current position
        """
        try:
            return PixelTool.get_color(self.surface, self.x, self.y)
        except IndexError:
            # If we're out of bounds, return a transparent black color
            return pygame.Color(0, 0, 0, 0)
    
    def get_pixel(self):
        """
        Get the pixel value at the current position.
        
        Returns:
            int: The pixel value
        """
        try:
            return PixelTool.get_pixel(self.surface, self.x, self.y)
        except IndexError:
            # If we're out of bounds, return 0 (usually transparent/black)
            return 0
    
    def put_color(self, color):
        """
        Set the color at the current position.
        
        Args:
            color (pygame.Color): The color to set
        """
        PixelTool.put_color(self.surface, self.x, self.y, color)
    
    def put_pixel(self, pixel):
        """
        Set the pixel value at the current position.
        
        Args:
            pixel (int): The pixel value to set
        """
        PixelTool.put_pixel(self.surface, self.x, self.y, pixel)