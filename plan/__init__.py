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
Plan package for the Fish Fillets NG game.
Contains components for game state management, planning, and dialog handling.
"""

from plan.command import Command
from plan.command_queue import CommandQueue
from plan.console_input import ConsoleInput
from plan.dialog_script import DialogScript
from plan.fish_dialog import FishDialog
from plan.game_state import GameState
from plan.key_console import KeyConsole
from plan.key_desc import KeyDesc
from plan.keymap import Keymap
from plan.planner import Planner
from plan.script_cmd import ScriptCmd
from plan.state_input import StateInput
from plan.state_manager import StateManager
from plan.subtitle_agent import SubTitleAgent
from plan.title import Title

__all__ = [
    'Command',
    'CommandQueue',
    'ConsoleInput',
    'DialogScript',
    'FishDialog',
    'GameState',
    'KeyConsole',
    'KeyDesc',
    'Keymap',
    'Planner',
    'ScriptCmd',
    'StateInput',
    'StateManager',
    'SubTitleAgent',
    'Title'
]