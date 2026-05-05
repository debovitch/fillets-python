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
from gengine.random import Random

class EffectDisintegrate(ViewEffect):
    """
    Draw disintegrating skeleton.
    This effect gradually makes objects disappear by rendering fewer pixels over time.
    """
    
    NAME = "disintegrate"
    DISINT_START = 400  # Starting disintegration value
    DISINT_SPEED = 30   # Speed of disintegration (higher = faster)
    
    def __init__(self):
        """
        Initialize the disintegration effect.
        Start as not disintegrated.
        """
        self.disint = self.DISINT_START
    
    def get_name(self):
        """
        Get the name of the effect.
        
        Returns:
            str: The name of the effect
        """
        return self.NAME
    
    def update_effect(self):
        """
        Update the disintegration state.
        Decreases the disintegration value over time until it reaches 0.
        """
        if self.disint > 0:
            self.disint -= self.DISINT_SPEED
            if self.disint < 0:
                self.disint = 0
    
    def is_disintegrated(self):
        """
        Returns true for objects for which the disintegration effect is finished.
        
        Returns:
            bool: True if the object is fully disintegrated
        """
        return self.disint == 0
    
    def is_invisible(self):
        """
        Check if the effect makes the object invisible.
        
        Returns:
            bool: True if the object is invisible
        """
        return self.is_disintegrated()
    
    def blit(self, screen, surface, x, y):
        """
        Apply the disintegration effect.
        Draw only some pixels based on the current disintegration level.
        
        Args:
            screen (pygame.Surface): The screen to draw on
            surface (pygame.Surface): The surface to draw
            x (int): X coordinate
            y (int): Y coordinate
        """
        # In Pygame, we can use Surface.lock() directly, but we'll use our SurfaceLock
        # to maintain the same pattern as the original code
        with SurfaceLock(screen):
            with SurfaceLock(surface):
                for py in range(surface.get_height()):
                    for px in range(surface.get_width()):
                        # Determine whether to draw this pixel based on random value and disint level
                        if Random.a_byte(py * surface.get_width() + px) < self.disint:
                            color = PixelTool.get_color(surface, px, py)
                            # In the original, unused is alpha (255 = fully opaque)
                            if color.a == 255:
                                PixelTool.put_color(screen, x + px, y + py, color)