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

from gengine.drawable import Drawable
from effect.picture import Picture

class StatusDisplay(Drawable):
    """
    Shows status change by displaying a picture for a specified time.
    """
    
    def __init__(self):
        """
        Initialize the status display.
        """
        self.picture = None
        self.time = 0
    
    def display_status(self, new_picture, time):
        """
        Display this picture for the given number of times.
        
        Args:
            new_picture (Picture): The picture to display
            time (int): How long to display the picture (in frames)
        """
        self.picture = new_picture
        self.time = time
    
    def draw_on(self, screen):
        """
        Draw the status picture on the screen if time remains.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        if self.time > 0:
            self.time -= 1
            if self.picture:
                self.picture.draw_on(screen)