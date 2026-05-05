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
Base class for script users.
"""

from gengine.no_copy import NoCopy
from gengine.script.script_state import ScriptState
from gengine.path import Path
from gengine.resource.script_exception import ScriptException

class Scripter(NoCopy):
    """
    Base class for script users.
    Provides access to Lua scripting functionality.
    """
    
    def __init__(self):
        """Initialize a new scripter."""
        NoCopy.__init__(self)
        self.script = ScriptState()
        self.script.register_leader(self)
        
        # Register common functions
        self.register_common_functions()
    
    def register_common_functions(self):
        """Register common functions available to all scripts."""
        # Register base script functions
        from gengine.script.def_script import register_lua_functions
        register_lua_functions(self, self)
        
        # Register options functions
        from gengine.script.options_functions import register_lua_functions as register_options_functions
        register_options_functions(self)
        
        # Additional functions
        self.script.register_function("setPersistent", self.script_set_persistent)
    
    def script_include(self, file_path):
        """
        Execute a script file.
        
        Args:
            file_path (Path): Path to the script file
            
        Raises:
            ScriptException: If the script has an error
        """
        self.script.do_file(file_path)

    def script_do(self, input_str):
        """
        Execute a script string.

        Args:
            input_str (str): Lua source code to execute

        Raises:
            ScriptException: If the script has an error
        """
        self.script.do_string(input_str)
    
    
    
    def script_set_persistent(self, script_state, name, value):
        """
        Set a persistent parameter value.
        
        Args:
            script_state: The script state
            name (str): The parameter name
            value: The parameter value
            
        Returns:
            None
        """
        from gengine.agent.option_agent import OptionAgent
        OptionAgent.agent().set_persistent(name, value)
        return None
    
