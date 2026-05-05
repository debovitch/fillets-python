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
worldmap-script.py - Python translation of worldmap-script.cpp

Functions for the world map Lua script interface.
These functions are registered with the Lua interpreter to allow Lua scripts
to interact with the world map.
"""

from gengine.path import Path
from gengine.v2 import V2
from gengine.log import log_warning
from gengine.ex_info import ExInfo


def get_world(script_state):
    """
    Get the world branch from the script state.
    
    Args:
        script_state: The script state
        
    Returns:
        WorldBranch: The world branch associated with the script
    """
    # In the Python version, we pass the world_branch directly to the function
    # rather than retrieving it from the script state
    return script_state


def worldmap_add_desc(script_state, codename, lang, levelname, desc):
    """
    Add a level description to the world map.
    Lua: void worldmap_addDesc(codename, lang, levelname, desc)
    
    Args:
        script_state: The script state (WorldBranch instance)
        codename: The level code name
        lang: The language code
        levelname: The level name
        desc: The level description
        
    Returns:
        int: Always 0
    """
    from menu.level_desc import LevelDescItem
    world = get_world(script_state)
    
    # Create a new level description
    dialog = LevelDescItem(lang, levelname, desc)
    world.add_desc(codename, dialog)
    
    return 0


def branch_add_node(script_state, parent, codename, datafile, x, y, hidden=False, poster=""):
    """
    Add a new node to the world map.
    Lua: void branch_addNode(parent, codename, datafile, x, y, hidden=false, poster="")
    
    Args:
        script_state: The script state (WorldBranch instance)
        parent: The parent node code name
        codename: The node code name
        datafile: The level data file path
        x: The x coordinate
        y: The y coordinate
        hidden: Whether the node is hidden (default: False)
        poster: The poster image (default: "")
        
    Returns:
        int: Always 0
    """
    from menu.level_node import LevelNode
    world = get_world(script_state)
    
    # Create a new level node
    node = LevelNode(codename, Path.data_read_path(datafile), V2(x, y), poster)
    world.add_node(parent, node, hidden)
    
    return 0


def branch_set_ending(script_state, codename, datafile, poster=""):
    """
    Set the ending node for the world map.
    Lua: void branch_setEnding(codename, datafile, poster="")
    
    Args:
        script_state: The script state (WorldBranch instance)
        codename: The node code name
        datafile: The level data file path
        poster: The poster image (default: "")
        
    Returns:
        int: Always 0
    """
    from menu.level_node import LevelNode
    world = get_world(script_state)
    
    # Create a new level node for the ending
    node = LevelNode(codename, Path.data_read_path(datafile), V2(-1, -1), poster)
    world.set_ending(node)
    
    return 0


def node_best_solution(script_state, codename, moves, author):
    """
    Set the best solution for a level.
    Lua: void node_bestSolution(codename, moves, author)
    
    Args:
        script_state: The script state (WorldBranch instance)
        codename: The level code name
        moves: The number of moves
        author: The author of the solution
        
    Returns:
        int: Always 0
    """
    world = get_world(script_state)
    world.best_solution(codename, moves, author)
    
    return 0

# Register all functions with the Lua interpreter
def register_lua_functions(script_agent, world_branch):
    """
    Register all world map functions with the Lua interpreter.
    
    Args:
        script_agent: The script agent
        world_branch: The world branch
    """
    script = script_agent.script
    
    # Register worldmap functions
    script.register_function("worldmap_addDesc", lambda state, *args: worldmap_add_desc(world_branch, *args))
    script.register_function("branch_addNode", lambda state, *args: branch_add_node(world_branch, *args))
    script.register_function("branch_setEnding", lambda state, *args: branch_set_ending(world_branch, *args))
    script.register_function("node_bestSolution", lambda state, *args: node_best_solution(world_branch, *args))
