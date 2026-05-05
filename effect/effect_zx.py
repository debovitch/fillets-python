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
from enum import Enum
from effect.view_effect import ViewEffect
from effect.surface_lock import SurfaceLock
from effect.pixel_tool import PixelTool
from effect.pixel_iterator import PixelIterator
from gengine.v2 import V2
from gengine.random import Random

class EffectZx(ViewEffect):
    """
    ZX Spectrum loading effect.
    Creates a blinking effect with colored stripes like old ZX Spectrum loading screens.
    """
    
    # Corner enumerations
    class Corner(Enum):
        ZX1 = 1
        ZX2 = 2
        ZX3 = 3
        ZX4 = 4
    
    NAME = "zx"
    STRIPE_STANDARD = 38.5
    STRIPE_NARROW = 3.4
    
    def __init__(self):
        """
        Initialize the ZX effect with colors from all four corners.
        """
        self.zx = self.Corner.ZX1
        self.phase = 0
        self.count_height = 0
        self.stripe_height = self.STRIPE_STANDARD
    
    def get_name(self):
        """
        Get the name of the effect.
        
        Returns:
            str: The name of the effect
        """
        return self.NAME
    
    def update_effect(self):
        """
        Update stripe height as ZX Spectrum does.
        Animates the ZX loading effect.
        """
        self.phase = (self.phase + 1) % 500
        
        if self.phase == 1:
            self.zx = self.Corner.ZX1
            self.stripe_height = self.STRIPE_STANDARD
        elif 2 <= self.phase <= 51:
            self.stripe_height = (self.stripe_height * 3 *
                                (0.97 + Random.random_real(0.06)) +
                                self.STRIPE_STANDARD) / 4.0
        elif self.phase == 52:
            self.zx = self.Corner.ZX3
            self.stripe_height = self.STRIPE_NARROW
        else:
            self.stripe_height = (self.stripe_height * 3 *
                                (0.95 + Random.random_real(0.1)) +
                                self.STRIPE_NARROW) / 4.0
    
    def blit(self, screen, surface, x, y):
        """
        Draw ZX spectrum loading effect.
        
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
                
                # Get colors from all four corners
                color_zx1 = PixelTool.get_color(surface, 0, 0)
                color_zx2 = PixelTool.get_color(surface, 0, height - 1)
                color_zx3 = PixelTool.get_color(surface, width - 1, 0)
                color_zx4 = PixelTool.get_color(surface, width - 1, height - 1)
                
                # Create a pixel iterator
                pit = PixelIterator(surface)
                
                for py in range(height):
                    self.count_height += 1
                    if self.count_height > self.stripe_height:
                        self.count_height -= self.stripe_height
                        # Switch to the next color
                        if self.zx == self.Corner.ZX1:
                            self.zx = self.Corner.ZX2
                        elif self.zx == self.Corner.ZX2:
                            self.zx = self.Corner.ZX1
                        elif self.zx == self.Corner.ZX3:
                            self.zx = self.Corner.ZX4
                        else:
                            self.zx = self.Corner.ZX3
                    
                    # Select the current color based on zx value
                    if self.zx == self.Corner.ZX1:
                        used_color = color_zx1
                    elif self.zx == self.Corner.ZX2:
                        used_color = color_zx2
                    elif self.zx == self.Corner.ZX3:
                        used_color = color_zx3
                    else:
                        used_color = color_zx4
                    
                    # Set the iterator to the beginning of this row
                    pit.set_pos(V2(0, py))
                    
                    for px in range(width):
                        if not pit.is_transparent():
                            PixelTool.put_color(screen, x + px, y + py, used_color)
                        pit.inc()