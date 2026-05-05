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
Handle input for pedometer.
Translated from PedoInput.h and PedoInput.cpp
"""

from state.game_input import GameInput

class PedoInput(GameInput):
    """
    Handle input for pedometer.
    Manages user interaction with the pedometer interface.
    """
    
    def __init__(self, pedometer):
        """
        Initialize a new pedometer input handler.
        
        Args:
            pedometer: The pedometer to control
        """
        GameInput.__init__(self, pedometer)
    
    def get_pedo(self):
        """
        Get the pedometer.
        
        Returns:
            The pedometer
        """
        from menu.pedometer import Pedometer
        return self.state if isinstance(self.state, Pedometer) else None
    
    def enable_subtitles(self):
        """Enable subtitles (not used in pedometer)."""
        pass
    
    def enable_help(self):
        """Enable help (not used in pedometer)."""
        pass
    
    def mouse_event(self, buttons):
        """
        Handle mouse events.
        
        Args:
            buttons: The mouse stroke event
        """
        if buttons.is_left():
            pedo = self.get_pedo()
            if pedo:
                pedo.run_selected()