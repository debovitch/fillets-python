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
Input handler that enables console and menu options.
"""

from plan.state_input import StateInput

class GameInput(StateInput):
    """
    Input handler which enables console and menu options.
    Base class for game input handlers.
    """
    
    def __init__(self, state):
        """
        Initialize a game input handler.
        
        Args:
            state: The game state to handle input for
        """
        StateInput.__init__(self, state)
    
    def enable_help(self):
        """
        Push help screen at top of the state stack.
        """
        from option.menu_help import MenuHelp
        self.state.push_state(MenuHelp())
    
    def enable_menu(self):
        """
        Push menu state at top of the state stack.
        """
        from option.menu_options import MenuOptions
        self.state.push_state(MenuOptions())