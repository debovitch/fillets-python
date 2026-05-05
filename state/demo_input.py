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
Input handler for demo mode.
"""

import pygame
from gengine.mouse_stroke import MouseStroke
from state.game_input import GameInput
from gengine.key_stroke import KeyStroke

class DemoInput(GameInput):
    """
    Input handler for demo playback.
    Accepts mouse clicks and key presses to exit the demo.
    """
    
    def __init__(self, demo):
        """
        Create a demo input handler.
        Escape, space or mouse click quit the state.
        
        Args:
            demo: Pointer to the leader state
        """
        GameInput.__init__(self, demo)
        
        # Add keymap attribute if it doesn't exist
        if not hasattr(self, 'keymap'):
            self.keymap = {}
            
        # Define KEY_QUIT constant if needed
        if not hasattr(self, 'KEY_QUIT'):
            self.KEY_QUIT = "quit"
    
    def enable_help(self):
        """
        Help is disabled in demo mode.
        """
        pass
    
    def _key_desc(self, index, desc):
        """
        Helper method to create a KeyDesc.
        
        Args:
            index: The key index
            desc: The key description
            
        Returns:
            KeyDesc: The key description
        """
        from plan.key_desc import KeyDesc
        return KeyDesc(index, desc)
    
    def mouse_event(self, buttons):
        """
        Handle mouse events - any click quits the state.
        
        Args:
            buttons: The mouse stroke
        """
        self.state.quit_state()
        return True