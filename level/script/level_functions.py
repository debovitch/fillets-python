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
level_functions.py - Python translation of level-script.cpp

Functions for the level Lua script interface.
These functions are registered with the Lua interpreter to allow Lua scripts
to interact with the level.
"""

from gengine.path import Path
from gengine.v2 import V2
from gengine.log import log_warning
from gengine.ex_info import ExInfo


def get_level_script(script_state):
    """
    Get the level script from the script state.
    
    Args:
        script_state: The script state
        
    Returns:
        LevelScript: The level script associated with the script
    """
    # In the Python version, we pass the level_script directly to the function
    return script_state


def get_level(script_state):
    """
    Get the level from the script state.
    
    Args:
        script_state: The script state
        
    Returns:
        Level: The level associated with the script
    """
    return get_level_script(script_state).level


def level_save(script_state, serialized):
    """
    Save the level.
    Lua: void level_save(serialized)
    
    Args:
        script_state: The script state (LevelScript instance)
        serialized: The serialized game state
        
    Returns:
        int: Always 0
    """
    get_level(script_state).save_game(serialized)
    return 0


def level_load(script_state, moves):
    """
    Load the level.
    Lua: void level_load(moves)
    
    Args:
        script_state: The script state (LevelScript instance)
        moves: The moves to load
        
    Returns:
        int: Always 0
    """
    get_level(script_state).load_game(moves)
    return 0


def level_action_move(script_state, symbol):
    """
    Perform a move action.
    Lua: bool level_action_move(symbol)
    
    Args:
        script_state: The script state (LevelScript instance)
        symbol: The move symbol
        
    Returns:
        bool: True if the move was successful
    """
    if len(symbol) != 1:
        log_warning(ExInfo("bad symbol length")
                  .add_info("length", len(symbol))
                  .add_info("symbol", symbol))
        raise ValueError(f"Bad symbol length: {len(symbol)}")
    
    success = get_level(script_state).action_move(symbol[0])
    return success


def level_action_save(script_state):
    """
    Perform a save action.
    Lua: bool level_action_save()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        bool: True if the save was successful
    """
    success = get_level(script_state).action_save()
    return success


def level_action_load(script_state):
    """
    Perform a load action.
    Lua: bool level_action_load()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        bool: True if the load was successful
    """
    success = get_level(script_state).action_load()
    return success


def level_action_restart(script_state):
    """
    Perform a restart action.
    Lua: bool level_action_restart()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        bool: True if the restart was successful
    """
    success = get_level(script_state).action_restart(1)
    return success


def level_create_room(script_state, w, h, picture):
    """
    Create a room.
    Lua: void level_createRoom(width, height, picture)
    
    Args:
        script_state: The script state (LevelScript instance)
        w: The width of the room
        h: The height of the room
        picture: The background picture
        
    Returns:
        int: Always 0
    """
    get_level(script_state).create_room(w, h, picture)
    return 0


def level_get_restart_counter(script_state):
    """
    Get the restart counter.
    Lua: int level_getRestartCounter()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        int: The restart counter
    """
    counter = get_level(script_state).get_restart_counter()
    return counter


def level_get_depth(script_state):
    """
    Get the level depth.
    Lua: int level_getDepth()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        int: The level depth
    """
    depth = get_level(script_state).get_depth()
    return depth


def level_is_new_round(script_state):
    """
    Check if this is a new round.
    Lua: bool level_isNewRound()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        bool: True if this is a new round
    """
    new_round = get_level(script_state).is_new_round()
    return new_round


def level_is_solved(script_state):
    """
    Check if the level is solved.
    Lua: bool level_isSolved()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        bool: True if the level is solved
    """
    solved = get_level_script(script_state).room().is_solved()
    return solved


def level_new_demo(script_state, demofile):
    """
    Create a new demo.
    Lua: void level_newDemo(demofile)
    
    Args:
        script_state: The script state (LevelScript instance)
        demofile: The demo file path
        
    Returns:
        int: Always 0
    """
    get_level(script_state).new_demo(Path.data_read_path(demofile))
    return 0


def level_plan_show(script_state, func_ref):
    """
    Plan a show action.
    Lua: void level_planShow(func)
    
    Args:
        script_state: The script state (LevelScript instance)
        func_ref: Reference to a Lua function
        
    Returns:
        int: Always 0
    """
    command = get_level_script(script_state).create_command(func_ref)
    get_level(script_state).plan_show(command)
    return 0


def level_is_showing(script_state):
    """
    Check if the level is showing.
    Lua: bool level_isShowing()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        bool: True if the level is showing
    """
    showing = get_level(script_state).is_showing()
    return showing


# Register all functions with the Lua interpreter
def register_lua_functions(script_agent, level_script):
    """
    Register all level functions with the Lua interpreter.
    
    Args:
        script_agent: The script agent
        level_script: The level script
    """
    script = script_agent.script
    
    # Register level functions
    script.register_function("level_save", lambda state, *args: level_save(level_script, *args))
    script.register_function("level_load", lambda state, *args: level_load(level_script, *args))
    
    script.register_function("level_action_move", lambda state, *args: level_action_move(level_script, *args))
    script.register_function("level_action_save", lambda state, *args: level_action_save(level_script))
    script.register_function("level_action_load", lambda state, *args: level_action_load(level_script))
    script.register_function("level_action_restart", lambda state, *args: level_action_restart(level_script))
    
    script.register_function("level_createRoom", lambda state, *args: level_create_room(level_script, *args))
    script.register_function("level_getRestartCounter", lambda state, *args: level_get_restart_counter(level_script))
    script.register_function("level_getDepth", lambda state, *args: level_get_depth(level_script))
    script.register_function("level_isNewRound", lambda state, *args: level_is_new_round(level_script))
    script.register_function("level_isSolved", lambda state, *args: level_is_solved(level_script))
    
    script.register_function("level_newDemo", lambda state, *args: level_new_demo(level_script, *args))
    script.register_function("level_planShow", lambda state, *args: level_plan_show(level_script, *args))
    script.register_function("level_isShowing", lambda state, *args: level_is_showing(level_script))
