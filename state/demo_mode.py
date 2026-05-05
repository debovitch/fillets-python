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
Graphical demo mode implementation.
"""

import pygame
from gengine.path import Path
from plan.game_state import GameState
from plan.planner import Planner
from gengine.drawable import Drawable
from state.demo_input import DemoInput
from effect.picture import Picture
from plan.subtitle_agent import SubTitleAgent
from gengine.agent.option_agent import OptionAgent
from gengine.agent.video_agent import VideoAgent
from effect.surface_tool import SurfaceTool

class DemoMode(Planner, GameState, Drawable):
    """
    Graphical demo playback.
    Loads and runs demo scripts.
    """
    
    def __init__(self, demoscript):
        """
        Initialize the demo mode.
        
        Args:
            demoscript (Path): Path to the demo script file
        """
        Planner.__init__(self)
        GameState.__init__(self)
        
        self.old_limit_y = 0
        self.demoscript = demoscript
        self.surface_buffer = None
        self.display = None
        
        # Create script environment
        from gengine.script.script_state import ScriptState
        self.script = ScriptState()

        from gengine.script.def_script import register_lua_functions
        from gengine.script.options_functions import register_lua_functions as register_options_functions
        from plan.dialog_script import DialogScript
        register_lua_functions(self, self)
        register_options_functions(self)
        DialogScript.register(self.script, self)
        
        # Register script functions
        self.script.register_function("demo_display", self.script_demo_display)
        self.script.register_leader(self)
        
        # Set up input and drawing
        self.take_handler(DemoInput(self))
    
    def __del__(self):
        """Clean up resources when deleted."""
        self.own_clean_state()
    
    def get_name(self):
        """
        Get the state name.
        
        Returns:
            str: The state name
        """
        return "state_demo"

    def script_include(self, file_path):
        """Execute a Lua script in the demo script environment."""
        self.script.do_file(file_path)
    
    def own_init_state(self):
        """Run the demo script and initialize state."""
        self.old_limit_y = SubTitleAgent.get_instance().get_limit_y()
        
        # Check if the script file exists
        if not hasattr(self.demoscript, 'exists') or not self.demoscript.exists():
            from gengine.log import log_warning
            log_warning(f"Demo script file not found: {self.demoscript}")
            # Create an empty surface
            from gengine.v2 import V2
            from gengine.agent.video_agent import VideoAgent
            from effect.picture import Picture
            import pygame
            
            # Create a surface with an error message
            surface = pygame.Surface((400, 300))
            surface.fill((0, 0, 0))  # Black background
            
            # Add error text
            font = pygame.font.SysFont(None, 24)
            text1 = font.render("Demo script not found:", True, (255, 255, 255))
            text2 = font.render(str(self.demoscript), True, (255, 255, 255))
            surface.blit(text1, (20, 100))
            surface.blit(text2, (20, 130))
            
            # Display the error surface
            self.display = Picture(surface, V2(0, 0))
        else:
            # Execute the demo script
            try:
                self.script.do_file(self.demoscript)
            except Exception as e:
                from gengine.log import log_error
                log_error(f"Error executing demo script: {e}")
                # We'll create an error picture in the catch block
    
    def own_update_state(self):
        """
        Execute next demo command.
        Quit when all commands are done.
        """
        if self.satisfy_plan():
            self.quit_state()
    
    def own_pause_state(self):
        """Pause the state (no-op)."""
        pass
    
    def own_resume_state(self):
        """Resume the state (no-op)."""
        pass
    
    def own_clean_state(self):
        """Clean up resources."""
        # Surface buffer cleanup is handled by Python's garbage collection
        self.surface_buffer = None
        
        if self.display:
            self.display = None
        
        SubTitleAgent.get_instance().set_limit_y(self.old_limit_y)
        self.kill_plan()
    
    def action_display(self, picture):
        """
        Store picture to draw it.
        
        Args:
            picture (Picture): The picture to display
            
        Returns:
            bool: True if successful
        """
        self.display = picture
        
        if self.surface_buffer is None:
            options = OptionAgent.get_instance()
            options.set_param("screen_width", self.display.get_w())
            options.set_param("screen_height", self.display.get_h())
            VideoAgent.get_instance().init_video_mode()
            
            SubTitleAgent.get_instance().set_limit_y(2 * self.display.get_h())
        
        return True
    
    def draw_on(self, screen):
        """
        Draw the demo on the screen.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        if self.surface_buffer is None:
            self.surface_buffer = SurfaceTool.create_empty(screen)
        
        if self.display:
            self.display.draw_on(self.surface_buffer)
        
        screen.blit(self.surface_buffer, (0, 0))
        if self.subtitle_agent:
            self.subtitle_agent.draw_on(screen)
    
    @staticmethod
    def script_demo_display(script_state, filename, x, y):
        """
        Script function to display a picture.
        
        Args:
            script_state: The script state
            filename (str): Path to the image file
            x (int): X coordinate
            y (int): Y coordinate
            
        Returns:
            None
        """
        from gengine.v2 import V2
        demo = script_state.get_leader()
        picture = Picture(Path.data_read_path(filename), V2(x, y))
        demo.action_display(picture)
        return None
