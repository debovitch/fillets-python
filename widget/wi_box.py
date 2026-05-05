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
from widget.i_widget import IWidget

class WiBox(IWidget):
    """
    Abstract box widget that contains other widgets.
    """
    
    def __init__(self):
        """
        Initialize an empty box.
        """
        super().__init__()
        self.widgets = []
    
    def add_widget(self, widget):
        """
        Add a widget to the box.
        
        Args:
            widget (IWidget): Widget to add
        """
        self.widgets.append(widget)
        self.update_layout()
    
    def update_layout(self):
        """
        Update the layout of widgets.
        Must be implemented by subclasses.
        """
        pass
    
    def set_shift(self, shift):
        """
        Set the box shift and update all widgets' shifts.
        
        Args:
            shift (V2): Position shift
        """
        super().set_shift(shift)
        self.update_layout()
    
    def own_get_tip(self, loc):
        """
        Get tooltip from contained widgets.
        
        Args:
            loc (V2): Mouse location
            
        Returns:
            str: Tooltip text
        """
        for widget in self.widgets:
            tip = widget.get_tip(loc.plus(self.shift))
            if tip:
                return tip
        return super().own_get_tip(loc)
    
    def own_mouse_button(self, stroke):
        """
        Pass mouse button event to all widgets.
        
        Args:
            stroke (MouseStroke): Mouse button event
        """
        for widget in self.widgets:
            widget.mouse_button(stroke)
    
    def draw_on(self, screen):
        """
        Draw all widgets.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        for widget in self.widgets:
            widget.draw_on(screen)