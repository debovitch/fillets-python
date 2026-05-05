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

class EffectMirror(ViewEffect):
    """
    Mirror effect that reflects the left side.
    This effect creates a mirror image by sampling pixels from the screen.
    """
    
    NAME = "mirror"
    MIRROR_BORDER = 3  # Width of the border that won't be mirrored
    
    def get_name(self):
        """
        Get the name of the effect.
        
        Returns:
            str: The name of the effect
        """
        return self.NAME
    
    def blit(self, screen, surface, x, y):
        """
        Apply the mirror effect.
        
        The pixel in the middle will be used as a mask.
        NOTE: mirror objects should be drawn last for the effect to work correctly.
        
        Args:
            screen (pygame.Surface): The screen to draw on
            surface (pygame.Surface): The surface to draw
            x (int): X coordinate
            y (int): Y coordinate
        """
        with SurfaceLock(screen):
            with SurfaceLock(surface):
                # Get the mask color from the middle of the surface
                width = surface.get_width()
                height = surface.get_height()
                mask = PixelTool.get_color(surface, width // 2, height // 2)
                
                # Process each pixel
                for py in range(height):
                    for px in range(width):
                        pixel = PixelTool.get_color(surface, px, py)
                        
                        if px > self.MIRROR_BORDER and PixelTool.color_equals(pixel, mask):
                            # Sample from the left side of the screen (mirror effect)
                            sample_x = x - px + self.MIRROR_BORDER
                            sample_y = y + py
                            
                            # Make sure the sample position is within the screen bounds
                            if (0 <= sample_x < screen.get_width() and 
                                0 <= sample_y < screen.get_height()):
                                sample = PixelTool.get_color(screen, sample_x, sample_y)
                                PixelTool.put_color(screen, x + px, y + py, sample)
                        else:
                            # Draw the normal pixel if it's not transparent
                            if pixel.a == 255:
                                PixelTool.put_color(screen, x + px, y + py, pixel)