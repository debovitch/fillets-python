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
def_script.py - Python translation of def-script.cpp and def-script.h

Common script utility functions.
"""

from gengine.path import Path
from gengine.ex_info import ExInfo


def script_get_leader_name():
    """
    Get the name of the script leader.
    
    Returns:
        str: The name of the script leader
    """
    return "script_leader"


def script_get_leader(script_state):
    """
    Get the script leader from the script state.
    
    Args:
        script_state: The script state
        
    Returns:
        Scripter: The script leader
        
    Raises:
        ValueError: If no leader is found
    """
    # In the Python implementation, we pass the script leader directly
    registry = script_state.get_registry()
    
    if script_get_leader_name() not in registry or registry[script_get_leader_name()] is None:
        raise ValueError(ExInfo("no leader").add_info("key", script_get_leader_name()).info())
        
    return registry[script_get_leader_name()]


def script_debug_stack(script_state, error_message=""):
    """
    Get a debug stack trace.
    
    Args:
        script_state: The script state
        error_message: The error message
        
    Returns:
        str: The stack trace
    """
    # In Python we can use the traceback module
    import traceback
    
    if not error_message:
        return ""
        
    stack_trace = "\nstack traceback:\n"
    stack_trace += "".join(traceback.format_stack())
    
    return error_message + stack_trace


def script_file_include(script_state, filename):
    """
    Include a script file.
    
    Args:
        script_state: The script state
        filename: The file to include
        
    Returns:
        int: Always 0
    """
    script_get_leader(script_state).script_include(Path.data_read_path(filename))
    return 0


def script_file_exists(script_state, filename):
    """
    Check if a file exists.
    
    Args:
        script_state: The script state
        filename: The file to check
        
    Returns:
        bool: True if the file exists
    """
    exists = Path.check_exists(Path.data_read_path(filename))
    return exists


# Register all functions with the Lua interpreter
def register_lua_functions(script_agent, script_leader):
    """
    Register all script utility functions with the Lua interpreter.
    
    Args:
        script_agent: The script agent
        script_leader: The script leader
    """
    script = script_agent.script
    
    # Store script leader in the registry
    registry = script.get_registry()
    registry[script_get_leader_name()] = script_leader
    
    # Register file functions
    script.register_function("file_include", lambda state, *args: script_file_include(state, *args))
    script.register_function("file_exists", lambda state, *args: script_file_exists(state, *args))
    
    # Register debug function
    script.register_function("debugStack", lambda state, *args: script_debug_stack(state, *args))