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
from gengine.drawable import Drawable
from gengine.v2 import V2
from gengine.resource.res_image_pack import ResImagePack

class Picture(Drawable):
    """
    Static picture at fixed screen position.
    Basic drawable that displays a static image.
    """
    
    def __init__(self, file_or_surface, loc):
        """
        Initialize the picture.
        
        Args:
            file_or_surface: Either a file path or a pygame.Surface
            loc (V2): The location of the picture on screen
        """
        self.loc = loc
        
        # Load the image or use the provided surface
        if isinstance(file_or_surface, pygame.Surface):
            self.surface = file_or_surface
        else:
            self.surface = ResImagePack.load_image(file_or_surface)
    
    def __del__(self):
        """
        Clean up resources when the object is deleted.
        """
        # In Python with Pygame, we don't need to explicitly free surfaces
        # as they will be garbage collected
        pass
    
    def get_w(self):
        """
        Get the width of the picture.
        
        Returns:
            int: The width in pixels
        """
        return self.surface.get_width()
    
    def get_h(self):
        """
        Get the height of the picture.
        
        Returns:
            int: The height in pixels
        """
        return self.surface.get_height()
    
    def draw_on(self, screen):
        """
        Draw the picture on the screen.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        screen.blit(self.surface, (self.loc.get_x(), self.loc.get_y()))
    
    def set_loc(self, loc):
        """
        Set the location of the picture.
        
        Args:
            loc (V2): The new location
        """
        self.loc = loc
    
    def change_picture(self, file_or_surface):
        """
        Change the picture to a new image.
        
        Args:
            file_or_surface: Either a file path or a pygame.Surface
        """
        # In Python with Pygame, we don't need to explicitly free surfaces
        
        # Load the new image or use the provided surface
        if isinstance(file_or_surface, pygame.Surface):
            self.surface = file_or_surface
        else:
            self.surface = ResImagePack.load_image(file_or_surface)