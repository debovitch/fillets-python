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
LayeredPicture class.
A picture with multiple layers and mask support.
"""

import pygame
from gengine.v2 import V2
from gengine.path import Path
from gengine.drawable import Drawable
from gengine.log import log_warning
from effect.picture import Picture
from effect.surface_lock import SurfaceLock

class LayeredPicture(Picture):
    """
    Picture with multiple layers and mask support.
    Used for interactive backgrounds with clickable areas.
    """
    
    MASK_NO = -1

    def __init__(self, upper_path, loc, lower_path=None, mask_path=None):
        """
        Initialize a new layered picture.
        
        Args:
            upper_path: Path to upper layer image
            loc: Location of the picture
            lower_path: Path to lower layer image (optional)
            mask_path: Path to mask image (optional)
        """
        # Load upper layer
        from gengine.log import log_debug, log_error
        
        try:
            if isinstance(upper_path, Path):
                # Log the file path for debugging
                # log_debug(f"Loading upper layer from: {upper_path.get_native()}")
                upper_path = upper_path.get_native()
            
            # Load the upper layer surface
            upper_surface = pygame.image.load(upper_path).convert_alpha()
            
            # Initialize with upper layer
            Picture.__init__(self, upper_surface, loc)
            
            # Initialize layers
            self.upper_surface = upper_surface
            self.lower_surface = None
            self.mask_surface = None
            self.active_mask = self.MASK_NO
            self._mask_overlay_cache = {}
            
            # log_debug(f"Successfully loaded upper layer: {upper_path}")
        except Exception as e:
            log_error(f"Failed to load upper layer: {upper_path}, error: {e}")
            # Create a default surface with error message
            surface = pygame.Surface((400, 300))
            surface.fill((255, 0, 0))  # Red background
            
            # Add error text
            font = pygame.font.SysFont(None, 24)
            text = font.render(f"ERROR: Failed to load image", True, (255, 255, 255))
            text2 = font.render(f"{upper_path}", True, (255, 255, 255))
            surface.blit(text, (20, 100))
            surface.blit(text2, (20, 130))
            
            # Initialize with error surface
            Picture.__init__(self, surface, loc)
            
            # Initialize layers
            self.upper_surface = surface
            self.lower_surface = None
            self.mask_surface = None
            self.active_mask = self.MASK_NO
            self._mask_overlay_cache = {}
        
        # Load lower layer if provided
        if lower_path:
            try:
                if isinstance(lower_path, Path):
                    # log_debug(f"Loading lower layer from: {lower_path.get_native()}")
                    lower_path = lower_path.get_native()
                
                self.lower_surface = pygame.image.load(lower_path).convert_alpha()
                
                # Make sure both surfaces have the same size
                if (self.upper_surface.get_width() != self.lower_surface.get_width() or
                    self.upper_surface.get_height() != self.lower_surface.get_height()):
                    log_warning(f"LayeredPicture layers have different sizes")
                    
                    # Resize lower surface
                    self.lower_surface = pygame.transform.scale(
                        self.lower_surface,
                        (self.upper_surface.get_width(), self.upper_surface.get_height())
                    )
                
                # log_debug(f"Successfully loaded lower layer: {lower_path}")
            except Exception as e:
                log_error(f"Failed to load lower layer: {lower_path}, error: {e}")
                # Create a default surface with same dimensions as upper surface
                self.lower_surface = pygame.Surface((self.upper_surface.get_width(), self.upper_surface.get_height()))
                self.lower_surface.fill((0, 0, 100))  # Dark blue for lower layer
        
        # Load mask if provided
        if mask_path:
            try:
                if isinstance(mask_path, Path):
                    # log_debug(f"Loading mask from: {mask_path.get_native()}")
                    mask_path = mask_path.get_native()
                
                self.mask_surface = pygame.image.load(mask_path).convert_alpha()
                # log_debug(f"Successfully loaded mask: {mask_path}")
            except Exception as e:
                log_error(f"Failed to load mask: {mask_path}, error: {e}")
                # Create a default mask with same dimensions as upper surface
                self.mask_surface = pygame.Surface((self.upper_surface.get_width(), self.upper_surface.get_height()), pygame.SRCALPHA)
                self.mask_surface.fill((0, 0, 0, 255))  # Black mask (no active areas)
    
    def get_mask_at(self, loc: V2) -> int:
        """
        Get the mask value at a specific position.
        
        Args:
            loc: The position to check
            
        Returns:
            object: The mask value at the position
        """
        if not self.mask_surface:
            return self.MASK_NO
        
        try:
            with SurfaceLock(self.mask_surface) as locked:
                # Get color at position (assuming 8-bit or 32-bit surface)
                if loc.get_x() >= 0 and loc.get_y() >= 0 and \
                   loc.get_x() < self.mask_surface.get_width() and \
                   loc.get_y() < self.mask_surface.get_height():
                    color = locked.get_at((int(loc.get_x()), int(loc.get_y())))
                    return tuple(color)
        except Exception as e:
            log_warning(f"Error getting mask at {loc.get_x()}, {loc.get_y()}: {e}")
        
        return self.MASK_NO
    
    def get_mask_at_world(self, loc: V2) -> int:
        """
        Get the mask value at a world position.
        
        Args:
            loc: The world position to check
            
        Returns:
            int: The mask value at the position
        """
        # Convert world position to local position
        local_x = loc.get_x() - self.loc.get_x()
        local_y = loc.get_y() - self.loc.get_y()
        
        return self.get_mask_at(V2(local_x, local_y))
    
    def get_no_mask(self) -> int:
        """
        Get the value for no mask.
        
        Returns:
            int: The value for no mask
        """
        return self.MASK_NO
    
    def set_active_mask(self, mask_value: int) -> None:
        """
        Set the active mask.
        
        Args:
            mask_value: The mask value to set
        """
        if mask_value != self.active_mask:
            self.active_mask = mask_value
    
    def set_no_active(self) -> None:
        """Set no active mask."""
        self.active_mask = self.get_no_mask()
    
    def draw_on(self, screen: pygame.Surface) -> None:
        """
        Draw the picture on a screen.
        
        Args:
            screen: The screen to draw on
        """
        screen.blit(self.surface, (self.loc.get_x(), self.loc.get_y()))
        if self.active_mask == self.get_no_mask() or not self.lower_surface or not self.mask_surface:
            return

        overlay = self._get_mask_overlay(self.active_mask)
        screen.blit(overlay, (self.loc.get_x(), self.loc.get_y()))

    def _get_mask_overlay(self, mask_value):
        """Return a cached lower-layer overlay containing only the active mask."""
        if mask_value in self._mask_overlay_cache:
            return self._mask_overlay_cache[mask_value]

        overlay = pygame.Surface(self.lower_surface.get_size(), pygame.SRCALPHA)
        width, height = self.mask_surface.get_size()

        for y in range(height):
            for x in range(width):
                if tuple(self.mask_surface.get_at((x, y))) == mask_value:
                    color = self.lower_surface.get_at((x, y))
                    if len(color) < 4 or color[3] == 255:
                        overlay.set_at((x, y), color)

        self._mask_overlay_cache[mask_value] = overlay
        return overlay
