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
Command which executes script function.
Translated from ScriptCmd.cpp
"""

from gengine.log import log_debug
from gengine.no_copy import NoCopy
from plan.command import Command

class ScriptCmd(Command, NoCopy):
    """Command which executes script function."""
    
    def __init__(self, script_state, func_ref):
        """
        Initialize a new script command.
        
        Args:
            script_state: The script state where to execute
            func_ref (int): Index of function at registry
        """
        Command.__init__(self)
        NoCopy.__init__(self)
        self.script_state = script_state
        self.func_ref = func_ref
    
    def __del__(self):
        """
        Remove function from registry.
        """
        try:
            self.script_state.unref(self.func_ref)
        except:
            pass
        
    def finish(self, count):
        """
        Return true when command has finished its work.
        
        Args:
            count (int): number of calls
            
        Returns:
            bool: true for finish
            
        Raises:
            ScriptException: when error occurs
        """
        return self.script_state.call_command(self.func_ref, count)