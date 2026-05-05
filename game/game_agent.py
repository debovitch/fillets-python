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
Game agent for Fish Fillets NG.
"""

import pygame
import time
from gengine.agent.base_agent import BaseAgent
from gengine.name import Name
from plan.state_manager import StateManager
from gengine.path import Path
from gengine.agent.option_agent import OptionAgent
from gengine.agent.input_agent import InputAgent
from gengine.key_stroke import KeyStroke
from gengine.key_binder import KeyBinder
from gengine.message.simple_msg import SimpleMsg
from gengine.log import log_debug, log_error
from menu.world_map import WorldMap
from level.level_status import LevelStatus
from level.level import Level
from menu.desc_finder import DescFinder

class GameAgent(BaseAgent):
    """
    Create and manage the game.
    Uses StateManager to manage WorldMap, Level, and other game states.
    """
    
    def __init__(self):
        """Initialize the game agent."""
        BaseAgent.__init__(self)
        self.manager = None
        
    def get_name(self):
        """
        Get the name of this agent.
        
        Returns:
            str: The name of the agent
        """
        return Name.GAME_NAME
    
    def own_init(self):
        """Initialize the game manager and push initial state."""
        self.manager = StateManager()
        
        # Check if we need to replay a solution
        options = OptionAgent.agent()
        replay_level = options.get_param("replay_level")
        
        if not replay_level:
            # Start with the world map
            worldmap_path = options.get_param("worldmap", "script/worldmap.lua")
            # Try to find the worldmap in the user_data directory
            path_map = Path.data_read_path(worldmap_path)
            worldmap = WorldMap()
            
            # Use Lua script to initialize the world map
            try:
                # log_debug(f"Attempting to initialize world map from {path_map.get_native()}")
                worldmap.init_map(path_map)
                # log_debug("World map initialized from Lua script")
                
            except Exception as e:
                log_error(f"Failed to initialize world map from Lua script: {e}")
                # Fallback to Python implementation if available
            
            self.manager.push_state(None, worldmap)
        else:
            # Replay a specific level solution
            self.replay_solution(replay_level)
        
        # Set up key bindings
        self.key_binding()
    
    def replay_solution(self, codename):
        """
        Replay a solution for the given level.
        Used only for testing.
        
        Args:
            codename (str): The level codename
        """
        # Use static variables to keep these objects between calls
        if not hasattr(GameAgent, 'level_status'):
            GameAgent.level_status = LevelStatus()
            GameAgent.desc = WorldMap()
        
        # Prepare level data
        GameAgent.level_status.prepare_run(codename, "", 0, "")
        moves = GameAgent.level_status.read_solved_moves()
        
        # Create and initialize the level
        datafile = Path.data_read_path(f"script/{codename}/init.lua")
        level = Level(codename, datafile, 0)
        level.fill_status(GameAgent.level_status)
        level.fill_desc(GameAgent.desc)
        
        # Push the level state and load the replay
        self.manager.push_state(None, level)
        level.load_replay(moves)
    
    def own_update(self):
        """Update the game state."""
        self.manager.update_game()
    
    def own_shutdown(self):
        """Save playtime and clean up resources."""
        options = OptionAgent.agent()
        playtime = options.get_as_int("playtime", 0)
        
        # Add current session time to total playtime (in seconds)
        playtime += int(time.time() - pygame.time.get_ticks() / 1000)
        options.set_persistent("playtime", playtime)
        
        # Clean up the manager
        self.manager = None
    
    def key_binding(self):
        """Set up global key bindings."""
        key_binder = InputAgent.agent().key_binder
        
        # Fullscreen toggle
        fs_key = KeyStroke(pygame.K_F11, 0)
        fs_msg = SimpleMsg(Name.VIDEO_NAME, "fullscreen")
        key_binder.add_stroke(fs_key, fs_msg)
        
        # Log level controls
        log_plus = KeyStroke(pygame.K_KP_PLUS, pygame.KMOD_RALT)
        log_plus_msg = SimpleMsg(Name.APP_NAME, "inc_loglevel")
        key_binder.add_stroke(log_plus, log_plus_msg)
        
        log_minus = KeyStroke(pygame.K_KP_MINUS, pygame.KMOD_RALT)
        log_minus_msg = SimpleMsg(Name.APP_NAME, "dec_loglevel")
        key_binder.add_stroke(log_minus, log_minus_msg)
    
    @staticmethod
    def get_instance():
        """
        Get the GameAgent instance.
        
        Returns:
            GameAgent: The singleton instance
        """
        from gengine.agent.agent_pack import AgentPack
        return AgentPack.get_agent(Name.GAME_NAME)
