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
Script agent for executing Lua scripts.
"""

from gengine.agent.base_agent import BaseAgent, agent_class
from gengine.name import Name
from gengine.script.scripter import Scripter
from gengine.path import Path
from gengine.resource.script_exception import ScriptException

@agent_class(Name.SCRIPT_NAME)
class ScriptAgent(BaseAgent, Scripter):
    """
    Agent for executing Lua scripts.
    Provides access to the Lua scripting engine.
    """
    
    def __init__(self):
        """Initialize the script agent."""
        BaseAgent.__init__(self)
        Scripter.__init__(self)
        
    def get_name(self):
        """
        Get the name of this agent.
        
        Returns:
            str: The name of the agent
        """
        return Name.SCRIPT_NAME
    
    def script_include(self, path):
        """
        Load and execute a script.
        
        Args:
            path (Path): Path to the script file
            
        Raises:
            ScriptException: If the script fails
        """
        try:
            self.script.do_file(path)
        except Exception as e:
            if isinstance(e, ScriptException):
                raise
            raise ScriptException(e.info() if hasattr(e, 'info') else str(e))
    
    # The agent() method will be provided by the agent_class decorator