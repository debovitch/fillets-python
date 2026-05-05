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
Scrolling poster display state.
"""

from gengine.v2 import V2
from state.poster_state import PosterState
from gengine.agent.option_agent import OptionAgent

class PosterScroller(PosterState):
    """
    Scroll very high pictures.
    Automatically scrolls the picture from bottom to top.
    """
    
    # Scrolling speed constant
    SHIFT_SPEED = 4
    
    def __init__(self, picture):
        """
        Initialize the poster scroller.
        
        Args:
            picture (Path): Path to the image file
        """
        PosterState.__init__(self, picture)
        self.shift = 0
        self.screen_h = 0
    
    def own_init_state(self):
        """Initialize the poster scroller."""
        # Keep the current video mode and scroll the tall poster through it.
        self.screen_h = OptionAgent.get_instance().get_as_int("screen_height")
        self.shift = -self.screen_h + self.SHIFT_SPEED
    
    def own_update_state(self):
        """
        Update the poster scroller.
        Scrolls the image and quits when done.
        """
        # Calculate the maximum shift based on the screen and image height
        max_shift = min(self.shift, self.bg.get_h() - self.screen_h//3)
        
        # Set the background location to create scrolling effect
        self.bg.set_loc(V2(0, -max_shift))
        
        # Increase shift for next frame
        self.shift += self.SHIFT_SPEED
        
        # Quit when we've scrolled past the end of the image
        if self.shift > self.bg.get_h():
            self.quit_state()
    
    def allow_bg(self):
        """
        Allow background to be visible.
        
        Returns:
            bool: Always True for poster scroller
        """
        return True
