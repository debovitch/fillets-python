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

from gengine.mouse_stroke import MouseStroke
from widget.i_widget import IWidget

class WiContainer(IWidget):
    """
    Container for other widgets with a border.
    """
    
    def __init__(self, content, border=0):
        """
        Initialize container with content and border.
        
        Args:
            content (IWidget): Content widget
            border (int): Border width
        """
        super().__init__()
        self.content = content
        self.border = border
    
    def get_w(self):
        """
        Get container width including border.
        
        Returns:
            int: Container width
        """
        return self.content.get_w() + 2 * self.border
    
    def get_h(self):
        """
        Get container height including border.
        
        Returns:
            int: Container height
        """
        return self.content.get_h() + 2 * self.border
    
    def set_shift(self, shift):
        """
        Set container shift and update content shift.
        
        Args:
            shift (V2): Position shift
        """
        super().set_shift(shift)
        content_shift = shift.plus(self.border, self.border)
        self.content.set_shift(content_shift)
    
    def own_get_tip(self, loc):
        """
        Get tooltip from content.
        
        Args:
            loc (V2): Mouse location
            
        Returns:
            str: Tooltip text
        """
        content_tip = self.content.get_tip(loc.plus(self.shift))
        if content_tip:
            return content_tip
        return super().own_get_tip(loc)
    
    def own_mouse_button(self, stroke):
        """
        Pass mouse button event to content.
        
        Args:
            stroke (MouseStroke): Mouse button event
        """
        self.content.mouse_button(stroke)
    
    def draw_on(self, screen):
        """
        Draw container and content.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        # Draw content first (will be below any border)
        self.content.draw_on(screen)