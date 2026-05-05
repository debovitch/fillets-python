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
Input handler for the help overlay.
"""

from plan.state_input import StateInput


class HelpInput(StateInput):
    """
    Close the help overlay on any key press or mouse click.
    """

    def __init__(self, state):
        """
        Initialize help input.

        Args:
            state: Help menu state
        """
        StateInput.__init__(self, state)

    def key_pressed(self, keystroke):
        """
        Handle any key by closing the help overlay.

        Args:
            keystroke: The key stroke

        Returns:
            bool: Always True
        """
        self.state.quit_state()
        return True

    def mouse_event(self, mouse_stroke):
        """
        Handle any mouse click by closing the help overlay.

        Args:
            mouse_stroke: The mouse event

        Returns:
            bool: Always True
        """
        self.state.quit_state()
        return True
