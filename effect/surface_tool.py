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

class SurfaceTool:
    """
    Surface utilities for Pygame.
    Provides methods for creating and manipulating surfaces.
    """
    
    @staticmethod
    def create_empty(surface, width=0, height=0):
        """
        Create a new empty surface with the same format as another surface.
        
        Args:
            surface (pygame.Surface): The surface to copy the format from
            width (int): The width of the new surface (0 for same as surface)
            height (int): The height of the new surface (0 for same as surface)
            
        Returns:
            pygame.Surface: A new empty surface
            
        Raises:
            pygame.error: If the surface cannot be created
        """
        if not width:
            width = surface.get_width()
        if not height:
            height = surface.get_height()
        
        # Create a new surface with the same format
        try:
            # Get the format details from the source surface
            depth = surface.get_bitsize()
            flags = 0
            
            # Check if the surface has alpha
            if surface.get_flags() & pygame.SRCALPHA:
                flags |= pygame.SRCALPHA
            
            # Create a new surface with the same properties
            new_surface = pygame.Surface((width, height), flags, depth)
            
            # If the original surface has per-pixel alpha, make sure the new one does too
            if surface.get_flags() & pygame.SRCALPHA:
                new_surface = new_surface.convert_alpha()
            else:
                new_surface = new_surface.convert()
                
            return new_surface
        except pygame.error as e:
            raise pygame.error(f"Failed to create empty surface: {str(e)}")
    
    @staticmethod
    def create_transparent(width, height, transparent_color):
        """
        Create a new transparent surface.
        
        Args:
            width (int): The width of the surface
            height (int): The height of the surface
            transparent_color (pygame.Color): The color to use as transparent
            
        Returns:
            pygame.Surface: A new transparent surface
            
        Raises:
            pygame.error: If the surface cannot be created
        """
        try:
            # Create a surface with per-pixel alpha
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Fill with transparent color
            SurfaceTool.alpha_fill(surface, None, transparent_color)
            
            return surface
        except pygame.error as e:
            raise pygame.error(f"Failed to create transparent surface: {str(e)}")
    
    @staticmethod
    def create_clone(surface):
        """
        Create a clone of a surface.
        
        Args:
            surface (pygame.Surface): The surface to clone
            
        Returns:
            pygame.Surface: A new cloned surface
            
        Raises:
            pygame.error: If the surface cannot be cloned
        """
        try:
            # In Pygame, copy() creates a new surface with the same properties
            return surface.copy()
        except pygame.error as e:
            raise pygame.error(f"Failed to clone surface: {str(e)}")
    
    @staticmethod
    def alpha_fill(surface, dstrect, color):
        """
        Fill a surface with a color, supporting alpha transparency.
        
        Args:
            surface (pygame.Surface): The surface to fill
            dstrect (pygame.Rect or None): The rectangle to fill, or None for the whole surface
            color (pygame.Color): The color to fill with, including alpha
            
        Raises:
            pygame.error: If the fill operation fails
        """
        try:
            # Determine the area to fill
            width = surface.get_width()
            height = surface.get_height()
            
            rect = None
            if dstrect:
                rect = pygame.Rect(dstrect)
                width = rect.width
                height = rect.height
            
            # Create a canvas with the right size
            canvas = SurfaceTool.create_empty(surface, width, height)
            
            # Fill the canvas with the RGB part of the color
            canvas.fill((color.r, color.g, color.b))
            
            # Set the alpha value
            canvas.set_alpha(color.a)
            
            # Blit the canvas onto the surface
            surface.blit(canvas, rect if rect else (0, 0))
        except pygame.error as e:
            raise pygame.error(f"Failed to fill surface: {str(e)}")