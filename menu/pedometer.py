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
Pedometer with tree buttons.
Translated from Pedometer.h and Pedometer.cpp
"""

import pygame
from gengine.v2 import V2
from gengine.path import Path
from plan.game_state import GameState
from gengine.drawable import Drawable
from effect.picture import Picture
from effect.layered_picture import LayeredPicture
from gengine.resource.res_image_pack import ResImagePack
from menu.node_drawer import NodeDrawer
from menu.solver_drawer import SolverDrawer
from menu.pedo_input import PedoInput
from gengine.agent.option_agent import OptionAgent
from gengine.message.string_msg import StringMsg

class Pedometer(GameState, Drawable):
    """
    Pedometer with three buttons.
    Shows the steps count for a solved level and options to play or replay.
    """
    
    def __init__(self, status, level):
        """
        Initialize a new pedometer.
        
        Args:
            status: The level status
            level: The level to play
        """
        GameState.__init__(self)
        self.level = level
        self.status = status
        self.solution = self.status.read_solved_moves()
        self.meter_phase = 0
        
        # Load backgrounds and resources
        self.prepare_bg()
        self.prepare_rack()
        
        # Load numbers
        self.numbers = ResImagePack.load_image(
            Path.data_read_path("images/menu/numbers.png")
        )
        
        # Set up input and drawables
        self.handler = PedoInput(self)
        self.take_handler(self.handler)
        self.register_drawable(self.bg)
        self.register_drawable(self.rack)
        self.register_drawable(self)
    
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'level') and self.level:
            del self.level
        if hasattr(self, 'numbers') and self.numbers:
            self.numbers = None
        if hasattr(self, 'rack') and self.rack:
            del self.rack
        if hasattr(self, 'bg') and self.bg:
            del self.bg
    
    def get_name(self):
        """
        Get the name of this state.
        
        Returns:
            str: The state name
        """
        return "state_pedometer"
    
    def prepare_bg(self):
        """Draw level name on background."""
        bg_surface = ResImagePack.load_image(
            Path.data_read_path("images/menu/map.png")
        )
        
        drawer = NodeDrawer()
        drawer.set_screen(bg_surface)
        drawer.draw_selected(self.level.get_level_name())
        
        solver = SolverDrawer(self.status)
        solver.set_shift(V2(
            (bg_surface.get_width() - solver.get_w()) / 2,
            bg_surface.get_height() - 150
        ))
        solver.draw_on(bg_surface)
        
        if hasattr(self, 'bg') and self.bg:
            self.bg.change_picture(bg_surface)
        else:
            self.bg = Picture(bg_surface, V2(0, 0))
    
    def prepare_rack(self):
        """Prepare buttons rack."""
        POS_X = 193
        POS_Y = 141
        
        self.rack = LayeredPicture(
            Path.data_read_path("images/menu/pedometer.png"),
            V2(POS_X, POS_Y),
            Path.data_read_path("images/menu/pedometer_lower.png"),
            Path.data_read_path("images/menu/pedometer_mask.png")
        )
        
        # Get mask values for buttons
        self.mask_run = self.rack.get_mask_at(V2(86, 100))
        self.mask_replay = self.rack.get_mask_at(V2(128, 100))
        self.mask_cancel = self.rack.get_mask_at(V2(170, 100))
        self.active_mask = self.rack.get_no_mask()
    
    def own_init_state(self):
        """Display menu and play menu music."""
        # Register for language changes
        self.register_watcher("lang")
        self.own_resume_state()
    
    def own_update_state(self):
        """Update the pedometer state."""
        self.watch_cursor()
    
    def own_pause_state(self):
        """Pause the pedometer state."""
        pass
    
    def own_resume_state(self):
        """Resume the pedometer state."""
        pass
    
    def own_clean_state(self):
        """Clean up resources."""
        pass
    
    def watch_cursor(self):
        """Check mouse position and mark button under cursor as active."""
        mouse_loc = self.get_input().get_mouse_loc()
        self.active_mask = self.rack.get_mask_at_world(mouse_loc)
        
        if (self.active_mask == self.mask_run or
            self.active_mask == self.mask_replay or
            self.active_mask == self.mask_cancel):
            self.rack.set_active_mask(self.active_mask)
        else:
            self.rack.set_no_active()
    
    def run_selected(self):
        """Start selected button action."""
        if self.active_mask == self.mask_run:
            self.run_level()
        elif self.active_mask == self.mask_replay:
            self.run_replay()
        else:
            self.quit_state()
    
    def run_level(self):
        """Start the level normally."""
        level_state = self.level
        self.level = None  # Prevent deletion in __del__
        
        poster = self.status.create_poster()
        if poster:
            poster.set_next_state(level_state)
            self.change_state(poster)
        else:
            self.change_state(level_state)
    
    def run_replay(self):
        """Start the level in replay mode."""
        level_state = self.level
        self.level = None  # Prevent deletion in __del__
        
        self.change_state(level_state)
        level_state.load_replay(self.solution)
    
    def draw_on(self, screen):
        """
        Draw the pedometer.
        
        Args:
            screen: The screen to draw on
        """
        self.bg.draw_on(screen)
        self.rack.draw_on(screen)
        self.draw_numbers(screen, len(self.solution))
    
    def draw_numbers(self, screen, value):
        """
        Draw number of steps with nice rotating animation.
        
        Args:
            screen: The screen to draw on
            value: The value to display
        """
        CIPHERS = 5
        POS_X = 275
        POS_Y = 177
        SHIFT_SPEED = 8
        
        number_width = self.numbers.get_width()
        number_height = self.numbers.get_height() // 10
        
        for i in range(CIPHERS - 1, -1, -1):
            cipher = value % 10
            value //= 10
            x = POS_X + number_width * i
            shift_y = max(
                number_height * (9 - cipher),
                number_height * 9 - SHIFT_SPEED * self.meter_phase
            )
            self.meter_phase += 1
            
            self.draw_number(screen, x, POS_Y, shift_y)
    
    def draw_number(self, screen, x, y, shift_y):
        """
        Draw a single number digit.
        
        Args:
            screen: The screen to draw on
            x: X position
            y: Y position
            shift_y: Y shift in the numbers image
        """
        dest_rect = pygame.Rect(x, y, 0, 0)
        
        src_rect = pygame.Rect(
            0, shift_y, 
            self.numbers.get_width(), 
            self.numbers.get_height() // 10
        )
        
        screen.blit(self.numbers, dest_rect, src_rect)
    
    def receive_string(self, msg):
        """
        Handle incoming messages.
        
        Args:
            msg: The message
        """
        if msg.equals_name("param_changed"):
            param = msg.get_value()
            if param == "lang":
                self.prepare_bg()
            else:
                from gengine.exceptions import UnknownMsgException
                raise UnknownMsgException(msg)
        else:
            from gengine.exceptions import UnknownMsgException
            raise UnknownMsgException(msg)

    def register_watcher(self, name):
        """
        Register a watcher for parameter changes.

        Args:
            name (str): Parameter name
        """
        msg = StringMsg(self, "param_changed", name)
        OptionAgent.agent().add_watcher(name, msg)
