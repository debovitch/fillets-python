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

class SurfaceLock:
    """
    Context manager for locking and unlocking Pygame surfaces.
    This replaces the RAII pattern used in C++ with a Python context manager.
    """
    
    def __init__(self, surface):
        """
        Initialize the surface lock.
        
        Args:
            surface (pygame.Surface): The surface to lock
        """
        self.surface = surface
    
    def __enter__(self):
        """
        Lock the surface if necessary.
        
        Returns:
            pygame.Surface: The locked surface
        
        Raises:
            pygame.error: If the surface cannot be locked
        """
        # In Pygame, not all surfaces need locking
        if self.surface.get_locked():
            # Already locked
            return self.surface
            
        try:
            self.surface.lock()
        except pygame.error as e:
            raise pygame.error(f"Failed to lock surface: {str(e)}")
        
        return self.surface
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Unlock the surface.
        
        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        if self.surface.get_locked():
            self.surface.unlock()