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
options_functions.py - Python translation of options-script.cpp

Functions for options-related script operations.
"""

from gengine.ex_info import ExInfo


def options_send_msg(script_state, listener, msg, value=None):
    """
    Send a message to a listener.
    Lua: void sendMsg(listener, msg, [value])
    
    Args:
        script_state: The script state
        listener: The listener name
        msg: The message name
        value: The message value (optional)
        
    Returns:
        int: Always 0
    """
    from gengine.agent.messager_agent import MessagerAgent
    from gengine.message.simple_msg import SimpleMsg
    from gengine.message.string_msg import StringMsg
    from gengine.message.int_msg import IntMsg
    
    message = None
    if isinstance(value, str):
        message = StringMsg(listener, msg, value)
    elif isinstance(value, (int, float)):
        message = IntMsg(listener, msg, int(value))
    else:
        message = SimpleMsg(listener, msg)
    
    MessagerAgent.agent().forward_new_msg(message)
    return 0


def options_set_param(script_state, name, value):
    """
    Set a parameter value.
    Lua: void setParam(name, value)
    
    Args:
        script_state: The script state
        name: The parameter name
        value: The parameter value
        
    Returns:
        int: Always 0
    """
    from gengine.agent.option_agent import OptionAgent
    OptionAgent.agent().set_param(name, str(value))
    return 0


def options_get_param(script_state, name):
    """
    Get a parameter value.
    Lua: string getParam(name)
    
    Args:
        script_state: The script state
        name: The parameter name
        
    Returns:
        str: The parameter value, or None if not found
    """
    from gengine.agent.option_agent import OptionAgent
    value = OptionAgent.agent().get_param(name)
    if not value:
        return None
    return value


# Register all functions with the Lua interpreter
def register_lua_functions(script_agent):
    """
    Register all options functions with the Lua interpreter.
    
    Args:
        script_agent: The script agent
    """
    script = script_agent.script
    
    # Register options functions
    script.register_function("sendMsg", options_send_msg)
    script.register_function("setParam", options_set_param)
    script.register_function("getParam", options_get_param)
    script.register_function("options_sendMsg", options_send_msg)
    script.register_function("options_setParam", options_set_param)
    script.register_function("options_getParam", options_get_param)
