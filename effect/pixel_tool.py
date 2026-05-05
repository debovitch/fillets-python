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
from effect.surface_lock import SurfaceLock

class PixelTool:
    """
    Utility class for pixel manipulation in Pygame surfaces.
    """
    
    @staticmethod
    def color_equals(color1, color2):
        """
        Compare two colors for equality.
        
        Args:
            color1 (pygame.Color): The first color
            color2 (pygame.Color): The second color
            
        Returns:
            bool: True if the colors are equal, False otherwise
        """
        return (color1.r == color2.r and 
                color1.g == color2.g and 
                color1.b == color2.b and 
                color1.a == color2.a)
    
    @staticmethod
    def get_color(surface, x, y):
        """
        Get the color at the given position.
        
        Args:
            surface (pygame.Surface): The surface to get the color from
            x (int): X coordinate
            y (int): Y coordinate
            
        Returns:
            pygame.Color: The color at the given position
        """
        with SurfaceLock(surface):
            return pygame.Color(*surface.get_at((x, y)))
    
    @staticmethod
    def put_color(surface, x, y, color):
        """
        Set the color at the given position.
        
        Args:
            surface (pygame.Surface): The surface to set the color on
            x (int): X coordinate
            y (int): Y coordinate
            color (pygame.Color): The color to set
        """
        # Make sure x and y are within the surface bounds
        if x < 0 or x >= surface.get_width() or y < 0 or y >= surface.get_height():
            return
            
        with SurfaceLock(surface):
            surface.set_at((x, y), color)
    
    @staticmethod
    def get_pixel(surface, x, y):
        """
        Get the pixel value at the given position.
        
        Args:
            surface (pygame.Surface): The surface to get the pixel from
            x (int): X coordinate
            y (int): Y coordinate
            
        Returns:
            int: The pixel value at the given position
        """
        with SurfaceLock(surface):
            return surface.get_at_mapped((x, y))
    
    @staticmethod
    def put_pixel(surface, x, y, pixel):
        """
        Set the pixel value at the given position.
        
        Args:
            surface (pygame.Surface): The surface to set the pixel on
            x (int): X coordinate
            y (int): Y coordinate
            pixel (int): The pixel value to set
        """
        # Pygame doesn't have a direct set_at_mapped equivalent,
        # so we need to convert the pixel value to a color
        color = pygame.Color(0, 0, 0, 0)
        color.r = (pixel >> 16) & 0xFF
        color.g = (pixel >> 8) & 0xFF
        color.b = pixel & 0xFF
        color.a = (pixel >> 24) & 0xFF
        
        PixelTool.put_color(surface, x, y, color)