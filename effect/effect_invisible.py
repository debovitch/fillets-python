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

class EffectInvisible(ViewEffect):
    """
    Invisible effect that doesn't draw anything.
    This effect makes an object completely invisible by not drawing it at all.
    """
    
    NAME = "invisible"
    
    def get_name(self):
        """
        Get the name of the effect.
        
        Returns:
            str: The name of the effect
        """
        return self.NAME
    
    def is_invisible(self):
        """
        Check if the effect makes the object invisible.
        
        Returns:
            bool: Always returns True for this effect
        """
        return True
    
    def blit(self, screen, surface, x, y):
        """
        Does nothing - the object is invisible.
        
        Args:
            screen (pygame.Surface): The screen to draw on
            surface (pygame.Surface): The surface to draw
            x (int): X coordinate
            y (int): Y coordinate
        """
        # Do nothing - the object is invisible
        pass