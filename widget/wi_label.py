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
Widget for displaying text labels.
Translated from WiLabel.h and WiLabel.cpp
"""

from widget.i_widget import IWidget

class WiLabel(IWidget):
    """
    Widget for displaying text labels.
    Renders and displays a single line of text.
    """
    
    def __init__(self, text, font, color):
        """
        Initialize a new label widget.
        
        Args:
            text: The label text
            font: The font to use
            color: The text color
        """
        IWidget.__init__(self)
        
        # Render the text
        self.surface = font.render_text(text, color)
        
        # Set widget dimensions
        self.w = self.surface.get_width()
        self.h = self.surface.get_height()
        
        # Set default alignment
        self.x_align = "left"
        self.center_x = False
    
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'surface') and self.surface:
            self.surface = None

    def get_w(self):
        """
        Get widget width.

        Returns:
            int: Widget width in pixels
        """
        return self.w

    def get_h(self):
        """
        Get widget height.

        Returns:
            int: Widget height in pixels
        """
        return self.h
    
    def set_x_align(self, align):
        """
        Set horizontal alignment.
        
        Args:
            align: The alignment ("left", "center", or "right")
        """
        self.x_align = align
    
    def draw_on(self, screen):
        """
        Draw the label on a surface.
        
        Args:
            screen: The surface to draw on
        """
        screen.blit(self.surface, (self.shift.get_x(), self.shift.get_y()))
