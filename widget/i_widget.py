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

from abc import abstractmethod
import pygame
from gengine.drawable import Drawable
from gengine.v2 import V2

class IWidget(Drawable):
    """
    Widget interface.
    Base class for all UI widgets.
    """
    
    def __init__(self):
        """Initialize widget."""
        self.shift = V2(0, 0)
        self.tip = ""
    
    @abstractmethod
    def get_w(self):
        """
        Get widget width.
        
        Returns:
            int: Widget width in pixels
        """
        pass
    
    @abstractmethod
    def get_h(self):
        """
        Get widget height.
        
        Returns:
            int: Widget height in pixels
        """
        pass
    
    def set_shift(self, shift):
        """
        Set widget position shift.
        
        Args:
            shift (V2): Position shift vector
        """
        self.shift = shift
    
    def set_tip(self, tip):
        """
        Set tooltip text.
        
        Args:
            tip (str): Tooltip text
        """
        self.tip = tip
    
    def own_mouse_button(self, stroke):
        """
        Handle mouse button event.
        
        Args:
            stroke (MouseStroke): Mouse button event
        """
        pass
    
    def own_get_tip(self, loc):
        """
        Get the tooltip for a location.
        
        Args:
            loc (V2): Mouse location
            
        Returns:
            str: Tooltip text
        """
        return self.tip
    
    def mouse_button(self, stroke):
        """
        Process mouse button event.
        
        Args:
            stroke (MouseStroke): Mouse button event
        """
        if self.is_inside(stroke.get_loc()):
            self.own_mouse_button(stroke)
    
    def get_tip(self, loc):
        """
        Get tooltip for a location.
        
        Args:
            loc (V2): Mouse location
            
        Returns:
            str: Tooltip text or empty string if mouse is not over the widget
        """
        if self.is_inside(loc):
            return self.own_get_tip(loc.minus(self.shift))
        return ""
    
    def is_inside(self, loc):
        """
        Check if location is inside the widget.
        
        Args:
            loc (V2): Location to check
            
        Returns:
            bool: True if location is inside the widget
        """
        x, y = loc.get_x(), loc.get_y()
        sx, sy = self.shift.get_x(), self.shift.get_y()
        return (sx <= x < sx + self.get_w() and 
                sy <= y < sy + self.get_h())