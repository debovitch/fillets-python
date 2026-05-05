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
from effect.view_effect import ViewEffect
from effect.surface_lock import SurfaceLock
from effect.pixel_tool import PixelTool

class EffectReverse(ViewEffect):
    """
    Reverse effect that swaps left and right sides.
    This effect mirrors the image horizontally.
    """
    
    NAME = "reverse"
    
    def get_name(self):
        """
        Get the name of the effect.
        
        Returns:
            str: The name of the effect
        """
        return self.NAME
    
    def blit(self, screen, surface, x, y):
        """
        Apply the reverse effect.
        Mirrors the image horizontally by inverting the x-coordinate.
        
        Args:
            screen (pygame.Surface): The screen to draw on
            surface (pygame.Surface): The surface to draw
            x (int): X coordinate
            y (int): Y coordinate
        """
        with SurfaceLock(screen):
            with SurfaceLock(surface):
                width = surface.get_width()
                height = surface.get_height()
                
                for py in range(height):
                    for px in range(width):
                        pixel = PixelTool.get_color(surface, px, py)
                        # Only draw non-transparent pixels
                        if pixel.a == 255:
                            # Calculate the reversed x position
                            reversed_x = x + width - 1 - px
                            PixelTool.put_color(screen, reversed_x, y + py, pixel)