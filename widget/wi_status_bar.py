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
from widget.i_widget import IWidget

class WiStatusBar(IWidget):
    """
    Status bar that displays text.
    """
    
    def __init__(self, font, color, width):
        """
        Initialize status bar.
        
        Args:
            font (pygame.font.Font): Text font
            color (tuple): Text color (r, g, b)
            width (int): Status bar width
        """
        super().__init__()
        self.font = font
        self.color = color
        self.width = width
        self.label = ""
        self.surface = None
        self.current_text = ""
    
    def get_w(self):
        """
        Get status bar width.
        
        Returns:
            int: Status bar width
        """
        return self.width
    
    def get_h(self):
        """
        Get status bar height.
        
        Returns:
            int: Status bar height
        """
        return self.font.get_height()
    
    def set_label(self, label):
        """
        Set status bar label.
        
        Args:
            label (str): Status text
        """
        if self.label != label:
            self.label = label
            if label:
                self.surface = self.font.render(label, True, self.color)
            else:
                self.surface = None
    
    def draw_on(self, screen):
        """
        Draw status bar.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        if self.surface:
            screen.blit(self.surface, (self.shift.get_x(), self.shift.get_y()))