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
level-script.py - Python translation of level-script.cpp and LevelScript.h/cpp

Functions for the level Lua script interface.
These functions are registered with the Lua interpreter to allow Lua scripts
to interact with the level.
"""

from gengine.path import Path
from gengine.v2 import V2
from gengine.log import log_warning
from gengine.ex_info import ExInfo
from plan.planner import Planner
from level.room_access import RoomAccess
from level.script.game_functions import register_lua_functions as register_game_lua_functions
from level.script.level_functions import register_lua_functions as register_level_lua_functions
from gengine.agent.sound_agent import SoundAgent
from plan.script_cmd import ScriptCmd
from plan.dialog_script import DialogScript
            
class LevelScript(Planner, RoomAccess):
    """
    Handle plan for dialogs and planned actions.
    Python translation of LevelScript.h/cpp.
    """
    
    def __init__(self, level):
        """
        Initialize a new level script.
        
        Args:
            level: The level
        """
        Planner.__init__(self)
        RoomAccess.__init__(self)
        self.level = level
        
    def register_lua_functions(self, script_state):
        """Register level/game/dialog functions into a level Lua state."""
        class ScriptOwner:
            def __init__(self, script):
                self.script = script

        owner = ScriptOwner(script_state)
        register_game_lua_functions(owner, self)
        register_level_lua_functions(owner, self)
        DialogScript.register(script_state, self)
    
    def update_script(self):
        """Update the script."""
        self.level.script_do("script_update()")
        self.update_plan()
    
    def interrupt_plan(self):
        """Interrupt the plan."""
        Planner.interrupt_plan(self)
    
    def create_command(self, func_ref):
        """
        Create a command from a Lua function reference.
        
        Args:
            func_ref: Reference to a Lua function
            
        Returns:
            Command: The created command
        """
        if not isinstance(func_ref, int):
            func_ref = self.level.script.ref(func_ref)
        return ScriptCmd(self.level.script, func_ref)
    
    def add_model(self, new_model, new_unit):
        """
        Add a model.
        
        Args:
            new_model: The new model
            new_unit: The new unit
            
        Returns:
            int: The model index
        """
        return self.room().add_model(new_model, new_unit)
    
    def get_model(self, model_index):
        """
        Get a model by index.
        
        Args:
            model_index: The model index
            
        Returns:
            Cube: The model
        """
        return self.room().get_model(model_index)
    
    def ask_field(self, loc):
        """
        Ask what's at a location.
        
        Args:
            loc: The location
            
        Returns:
            Cube: The model at the location
        """
        return self.room().ask_field(loc)
    
    def add_sound(self, name, file):
        """
        Add a sound.
        
        Args:
            name: The sound name
            file: The sound file path
        """
        self.room().add_sound(name, file)
    
    def play_sound(self, name, volume=100):
        """
        Play a sound.
        
        Args:
            name: The sound name
            volume: The volume (default: 100)
        """
        self.room().play_sound(name, volume)
