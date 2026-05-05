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

from widget.i_widget import IWidget

class WiSpace(IWidget):
    """
    Empty space widget for padding.
    """
    
    def __init__(self, width, height):
        """
        Initialize space with width and height.
        
        Args:
            width (int): Space width
            height (int): Space height
        """
        super().__init__()
        self.width = width
        self.height = height
    
    def get_w(self):
        """
        Get space width.
        
        Returns:
            int: Space width
        """
        return self.width
    
    def get_h(self):
        """
        Get space height.
        
        Returns:
            int: Space height
        """
        return self.height
    
    def draw_on(self, screen):
        """
        Draw nothing.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        pass  # Empty space doesn't draw anything