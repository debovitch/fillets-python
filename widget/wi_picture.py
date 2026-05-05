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
from gengine.path import Path
from widget.i_widget import IWidget

class WiPicture(IWidget):
    """
    Widget that displays an image.
    """
    
    def __init__(self, path):
        """
        Initialize with an image from path.
        
        Args:
            path (Path): Path to the image
        """
        super().__init__()
        self.surface = pygame.image.load(path.get_native())
    
    def get_w(self):
        """
        Get picture width.
        
        Returns:
            int: Picture width
        """
        return self.surface.get_width()
    
    def get_h(self):
        """
        Get picture height.
        
        Returns:
            int: Picture height
        """
        return self.surface.get_height()
    
    def draw_on(self, screen):
        """
        Draw the picture.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        screen.blit(self.surface, (self.shift.get_x(), self.shift.get_y()))