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
World map implementation.
Manages the menu with level nodes and navigation.
"""

import sys
import pygame
from typing import Optional, Dict, List

from gengine.v2 import V2
from gengine.path import Path
from gengine.drawable import Drawable
from gengine.exceptions import LogicException
from gengine.ex_info import ExInfo
from gengine.no_copy import NoCopy
from gengine.log import log_debug

from menu.level_node import LevelNode
from menu.node_drawer import NodeDrawer
from menu.level_desc import LevelDesc
from menu.world_input import WorldInput
from menu.desc_finder import DescFinder
from menu.world_branch import WorldBranch
from effect.layered_picture import LayeredPicture
from plan.game_state import GameState

class WorldMap(GameState, DescFinder):
    """
    Map with path from one level to another.
    Main menu interface.
    """
    
    def __init__(self):
        """Initialize a new world map."""
        GameState.__init__(self)
        
        # Initialize properties
        self.last_mouse_loc = V2(-1, -1)
        self.start_node = None
        self.selected = None
        self.ending = None
        self.drawer = NodeDrawer()
        self.desc_pack = None
        self.level_status = None
        
        # Prepare background and buttons
        self.prepare_bg()
        
        # Set up resources and input handler
        from gengine.resource.res_dialog_pack import ResDialogPack
        from level.level_status import LevelStatus
        
        self.desc_pack = ResDialogPack()
        self.level_status = LevelStatus()
        self.handler = WorldInput(self)
        self.take_handler(self.handler)
        
        # Register drawables
        self.drawables = []
        self.register_drawable(self.bg)
        self.register_drawable(self)
    
    def __del__(self):
        """Clean up resources."""
        self.clean_resources()
    
    def get_name(self) -> str:
        """
        Get the name of this state.
        
        Returns:
            str: The state name
        """
        return "state_worldmap"
    
    def prepare_bg(self) -> None:
        """Prepare background with buttons."""
        try:
            # Use LayeredPicture with map background and mask
            self.bg = LayeredPicture(
                Path.data_read_path("images/menu/map.png"),
                V2(0, 0),
                Path.data_read_path("images/menu/map_lower.png"),
                Path.data_read_path("images/menu/map_mask.png")
            )
            
            # Get masks for buttons
            self.mask_intro = self.bg.get_mask_at(V2(0, 0))
            self.mask_exit = self.bg.get_mask_at(V2(self.bg.get_w() - 1, 0))
            self.mask_credits = self.bg.get_mask_at(V2(0, self.bg.get_h() - 1))
            self.mask_options = self.bg.get_mask_at(V2(self.bg.get_w() - 1, self.bg.get_h() - 1))
            self.active_mask = self.bg.get_no_mask()
            
        except Exception as e:
            sys.exit(f"Failed to load menu background: {e}")  
    
    def init_map(self, mapfile: Path) -> None:
        """
        Read dot positions and level descriptions.
        
        Args:
            mapfile: The map file path
            
        Raises:
            LogicException: If the map file cannot be parsed
        """
        parser = WorldBranch(None)
        ending_ref = [self.ending]
        self.start_node = parser.parse_map(mapfile, ending_ref, self.desc_pack)
        self.ending = ending_ref[0]
        
        if self.start_node is None:
            raise LogicException(ExInfo("cannot create world map")
                              .add_info("file", mapfile.get_native()))
    
    def own_init_state(self) -> None:
        """Initialize the menu state."""
        self.level_status.set_running(True)
        self.own_resume_state()
    
    def own_update_state(self) -> None:
        """Update the menu state."""
        if self.ending and self.selected == self.ending:
            self.run_selected()
        else:
            self.watch_cursor()
    
    def own_pause_state(self) -> None:
        """Pause the menu state."""
        pass
    
    def own_resume_state(self) -> None:
        """Resume the menu state and play menu music."""
        next_level = None
        
        if self.level_status.was_running():
            if self.level_status.is_complete():
                self.mark_solved()
                if self.check_ending():
                    next_level = self.ending
            
            self.level_status.set_running(False)
            
            from gengine.agent.option_agent import OptionAgent
            from gengine.agent.video_agent import VideoAgent
            
            options = OptionAgent.agent()
            options.set_param("caption", self.find_desc("menu"))
            options.set_param("screen_width", self.bg.get_w())
            options.set_param("screen_height", self.bg.get_h())
            VideoAgent.agent().init_video_mode()
        
        self.selected = next_level
        
        # Play menu music
        from gengine.agent.sound_agent import SoundAgent
        SoundAgent.agent().play_music(
            Path.data_read_path("music/menu.ogg"), None
        )
    
    def own_clean_state(self) -> None:
        """Stop music and clean up."""
        from gengine.agent.sound_agent import SoundAgent
        SoundAgent.agent().stop_music()
        self.clean_resources()

    def clean_resources(self) -> None:
        """Release resources owned by the world map."""
        if self.start_node:
            del self.start_node
            self.start_node = None
        if self.ending:
            del self.ending
            self.ending = None
        if self.bg:
            del self.bg
            self.bg = None
        if self.desc_pack:
            self.desc_pack.remove_all()
            self.desc_pack = None
        if self.drawer:
            self.drawer.clean()
            self.drawer = None
        if self.level_status:
            del self.level_status
            self.level_status = None
    
    def watch_cursor(self) -> None:
        """Watch cursor position for level selection."""
        
        # Get mouse location 
        input_provider = self.get_input()
        if not input_provider:
            sys.exit("No input provider available")
            return
            
        mouse_loc = input_provider.get_mouse_loc()
        
        # Update selection if mouse has moved
        if not self.last_mouse_loc.equals(mouse_loc):
            self.last_mouse_loc = mouse_loc
            
            # Find if mouse is over a level node
            if self.start_node:
                self.selected = self.start_node.find_selected(mouse_loc)
                # if self.selected:
                    # log_debug(f"Selected node: {self.selected.get_codename()}")
                
            # Check for button masks in the background image
            old_mask = self.active_mask
            self.active_mask = self.bg.get_mask_at_world(mouse_loc)
            
            # if old_mask != self.active_mask:
                # log_debug(f"Mask changed from {old_mask} to {self.active_mask}")
            
            # Change the background when over buttons
            if (self.active_mask == self.mask_intro or
                self.active_mask == self.mask_exit or
                self.active_mask == self.mask_credits or
                self.active_mask == self.mask_options):
                self.bg.set_active_mask(self.active_mask)
            else:
                self.bg.set_no_active()
        
        # Check if left mouse button is pressed
        # if input_provider.is_left_pressed():
            # log_debug(f"Left mouse button is pressed at {mouse_loc}")
            # This will be handled by mouse_event in WorldInput
    
    def select_next_level(self) -> None:
        """Select the next available level."""
        self.selected = self.start_node.find_next_open(self.selected)
    
    def run_selected(self) -> None:
        """
        Start level under pressed button.
        Start pedometer when level is solved already.
        """
        from level.level import Level
        from gengine.log import log_debug
        
        # log_debug(f"Running selected: active_mask={self.active_mask}")
        
        level = self.create_selected()
        if level:
            log_debug(f"Starting level: {self.selected.get_codename()}")
            self.level_status.prepare_run(
                self.selected.get_codename(),
                self.selected.get_poster(),
                self.selected.get_best_moves(),
                self.selected.get_best_author()
            )
            level.fill_status(self.level_status)
            
            if self.selected.get_state() == LevelNode.STATE_SOLVED:
                from menu.pedometer import Pedometer
                pedometer = Pedometer(self.level_status, level)
                self.push_state(pedometer)
            else:
                self.push_state(level)
            return

        if self.active_mask == self.mask_intro:
            log_debug("Running intro")
            self.run_intro()
        elif self.active_mask == self.mask_exit:
            log_debug("Quitting")
            self.quit_state()
        elif self.active_mask == self.mask_credits:
            log_debug("Running credits")
            self.run_credits()
        elif self.active_mask == self.mask_options:
            log_debug("Running options")
            self.run_options()
        else:
            log_debug("No level selected")
    
    def create_selected(self):
        """
        Create a level from the selected node.
        
        Returns:
            Level: The created level or None
        """
        from level.level import Level
        
        result = None
        if self.selected:
            result = self.selected.create_level()
            result.fill_desc(self)
        
        return result
    
    def mark_solved(self) -> None:
        """Mark the current level as solved."""
        if self.selected:
            self.selected.set_state(LevelNode.STATE_SOLVED)
    
    def check_ending(self) -> bool:
        """
        Check if all levels are solved to allow the ending level.
        
        Returns:
            bool: True if ending should be started
        """
        result = False
        if self.ending and self.selected != self.ending:
            if self.selected.is_leaf():
                if self.start_node.are_all_solved():
                    result = True
        
        return result
    
    def draw_on(self, screen: pygame.Surface) -> None:
        """
        Draw the world map.
        
        Args:
            screen: The screen to draw on
        """
        # log_debug(f"Drawing world map on screen {screen.get_width()}x{screen.get_height()}")
        
        # Draw the background
        for drawable in self.drawables:
            if drawable != self:  # Avoid infinite recursion
                # log_debug(f"Drawing drawable {drawable.__class__.__name__}")
                drawable.draw_on(screen)
        
        # Set the screen for the drawer
        self.drawer.set_screen(screen)
        
        # Draw nodes and paths
        if self.start_node:
            # log_debug(f"Drawing start node paths")
            self.start_node.draw_path(self.drawer)
            
            # Draw selection
            if self.selected:
                # log_debug(f"Drawing selection")
                self.drawer.draw_select(self.selected.get_loc())
                self.drawer.draw_selected(self.find_level_name(self.selected.get_codename()))
        else:
            log_debug("No start node to draw")
    
    def draw_nodes(self, node: LevelNode) -> None:
        """
        Draw a node.
        
        Args:
            node: The node to draw
        """
        self.drawer.draw_node(node)
    
    def find_level_name(self, codename: str) -> str:
        """
        Find a level name by code name.
        
        Args:
            codename: The level code name
            
        Returns:
            str: The level name
        """
        result = ""
        desc = self.desc_pack.find_dialog_hard(codename)
        
        if desc:
            result = desc.get_level_name()
        else:
            result = codename
        
        return result
    
    def find_desc(self, codename: str) -> str:
        """
        Find a level description by code name.
        
        Args:
            codename: The level code name
            
        Returns:
            str: The level description
        """
        result = ""
        desc = self.desc_pack.find_dialog_hard(codename)
        
        if desc:
            result = desc.get_desc()
        else:
            result = "???"
        
        return result
    
    def run_intro(self) -> None:
        """Run the intro movie or demo."""
        from gengine.log import log_warning
        
        # Try to play movie
        movie_file = Path.data_read_path("images/menu/intro.mpg")

        if movie_file.exists():
            from state.movie_state import MovieState
            if MovieState.is_available():
                self.push_state(MovieState(movie_file))
                return
        else:
            log_warning(ExInfo("cannot find intro")
                      .add_info("file", movie_file.get_native()))

        # Fallback to demo mode
        from state.demo_mode import DemoMode
        self.push_state(DemoMode(Path.data_read_path("script/share/demo_intro.lua")))

    def run_credits(self) -> None:
        """Run the credits scroll."""
        from state.poster_scroller import PosterScroller
        self.push_state(PosterScroller(
            Path.data_read_path("images/menu/credits.png")
        ))
    
    def run_options(self) -> None:
        """Run the options menu."""
        from option.menu_options import MenuOptions
        options = MenuOptions()
        self.push_state(options)
    
    # GameState method implementations
    def register_drawable(self, drawable):
        """
        Register a drawable.
        
        Args:
            drawable: The drawable
        """
        if hasattr(self, 'drawables'):
            self.drawables.append(drawable)
    
    def get_input(self):
        """
        Get the input provider.
        
        Returns:
            The input provider
        """
        return self.handler.get_provider() if self.handler else None
    
    def push_state(self, new_state):
        """
        Push a new state onto the stack.
        
        Args:
            new_state: The new state
        """
        if self.manager:
            self.manager.push_state(self, new_state)
    
    def quit_state(self):
        """Quit this state."""
        if self.manager:
            self.manager.pop_state()
