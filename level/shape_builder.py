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
from level.shape import Shape
from level.cube import Cube
from level.view import View
from effect.surface_tool import SurfaceTool

class ShapeBuilder:
    """
    Creator of images from shapes.
    Useful for testing new levels.
    Not meant to be instantiated.
    """
    
    @staticmethod
    def prepare_color(shape, weight):
        """
        Prepare color values based on the given shape and weight.
        
        Args:
            shape (Shape): The shape to get color for
            weight (Cube.Weight): The weight of the shape
            
        Returns:
            pygame.Color: The color to use for the shape
        """
        color = pygame.Color(0, 0, 0, 255)
        
        if weight == Cube.Weight.LIGHT:
            g_value = ShapeBuilder.calc_shape_hash(shape) % 255
            color.g = g_value
            color.r = 255 - g_value
        elif weight == Cube.Weight.HEAVY:
            color.b = 50 + (ShapeBuilder.calc_shape_hash(shape) % (255 - 50))
        else:
            color.r = 128
            color.g = 128
            color.b = 128
            
        return color
    
    @staticmethod
    def calc_shape_hash(shape):
        """
        Calculate an almost unique hash of the shape.
        
        Args:
            shape (Shape): The shape to calculate hash for
            
        Returns:
            int: The hash value
        """
        hash_value = 0
        for mark in shape.get_rel_locs():
            hash_value = 31 * hash_value + mark.get_x()
            hash_value = 31 * hash_value + mark.get_y()
        return hash_value
    
    @staticmethod
    def create_image(shape, weight):
        """
        Create a new image for the given shape.
        
        Args:
            shape (Shape): The shape to create image for
            weight (Cube.Weight): The weight of the shape
            
        Returns:
            pygame.Surface: Surface with the shape image
        """
        # Define transparent color (magenta)
        transparent = pygame.Color(255, 0, 255, 255)
        
        # Create transparent surface directly with Pygame
        size = (shape.get_w() * View.SCALE, shape.get_h() * View.SCALE)
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((255, 0, 255))
        
        # Create rectangle for drawing marks
        rect = pygame.Rect(0, 0, View.SCALE, View.SCALE)
        
        # Prepare the color based on shape and weight
        color = ShapeBuilder.prepare_color(shape, weight)
        
        # Draw each mark of the shape
        for mark in shape.get_rel_locs():
            rect.x = mark.get_x() * View.SCALE
            rect.y = mark.get_y() * View.SCALE
            pygame.draw.rect(surface, color, rect)
        
        return surface