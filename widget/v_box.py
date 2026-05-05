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

from gengine.v2 import V2
from widget.wi_box import WiBox

class VBox(WiBox):
    """
    Vertical box that arranges widgets in a column.
    """
    
    def __init__(self):
        """
        Initialize an empty vertical box.
        """
        super().__init__()
        self.centered = False
    
    def get_w(self):
        """
        Get the maximum width of all widgets.
        
        Returns:
            int: Box width
        """
        if not self.widgets:
            return 0
        return max(widget.get_w() for widget in self.widgets)
    
    def get_h(self):
        """
        Get the total height of all widgets.
        
        Returns:
            int: Box height
        """
        return sum(widget.get_h() for widget in self.widgets)
    
    def update_layout(self):
        """
        Update the layout of widgets vertically.
        """
        x = self.shift.get_x()
        y = self.shift.get_y()
        width = self.get_w()
        
        for widget in self.widgets:
            widget_x = x
            if self.centered:
                widget_x += (width - widget.get_w()) // 2
            widget.set_shift(V2(widget_x, y))
            y += widget.get_h()
    
    def enable_centered(self):
        """Enable centered alignment for all widgets."""
        self.centered = True
        self.update_layout()
    
    def recenter(self):
        """Recenter widgets after changes."""
        self.update_layout()
