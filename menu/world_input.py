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

import pygame
from gengine.input_handler import (
    InputHandler,
    MOUSE_LEFT_MASK,
    MOUSE_MIDDLE_MASK,
    MOUSE_RIGHT_MASK,
)
from gengine.input_provider import InputProvider
from gengine.key_stroke import KeyStroke
from gengine.mouse_stroke import MouseStroke
from gengine.v2 import V2

class WorldInput(InputHandler):
    """
    Handle input for the world map.
    """
    
    # Key constants
    KEY_TAB = pygame.K_TAB
    KEY_ENTER = pygame.K_RETURN
    
    def __init__(self, world):
        """
        Initialize a new world input handler.
        
        Args:
            world: The world map
        """
        InputHandler.__init__(self)
        self.state = world
        self.provider = WorldInputProvider(world)
    
    def get_provider(self):
        """
        Get the input provider.
        
        Returns:
            InputProvider: The input provider
        """
        return self.provider
    
    def key_pressed(self, keystroke):
        """
        Handle key presses.
        
        Args:
            keystroke: The key that was pressed
            
        Returns:
            bool: True if the key was handled
        """
        return self.provider.key_pressed(keystroke)

    def key_up(self, keystroke):
        """
        Handle key releases.

        Args:
            keystroke: The key that was released

        Returns:
            bool: True if the key was handled
        """
        return self.provider.key_released(keystroke)
    
    def mouse_event(self, mouse_stroke):
        """
        Handle mouse events.
        
        Args:
            mouse_stroke: The mouse event
            
        Returns:
            bool: True if the event was handled
        """
        return self.provider.mouse_event(mouse_stroke)

    def mouse_state(self, loc, buttons):
        """Synchronize continuous mouse state with the worldmap provider."""
        super().mouse_state(loc, buttons)
        self.provider.mouse_state(loc, buttons)

class WorldInputProvider(InputProvider):
    """Input provider for the world map."""
    
    def __init__(self, world):
        """
        Initialize the input provider.
        
        Args:
            world: The world map
        """
        self.world = world
        self._pressed_keys = {}
        self._mouse_buttons = [False, False, False]  # left, middle, right
        self._mouse_loc = None
        pos = pygame.mouse.get_pos()
        self._mouse_loc = V2(pos[0], pos[1])

    def mouse_state(self, loc, buttons):
        """Update continuous mouse position and pressed buttons."""
        self._mouse_loc = loc if hasattr(loc, "get_x") else V2(loc[0], loc[1])

        if isinstance(buttons, (tuple, list)):
            self._mouse_buttons = [
                bool(buttons[0]) if len(buttons) > 0 else False,
                bool(buttons[1]) if len(buttons) > 1 else False,
                bool(buttons[2]) if len(buttons) > 2 else False,
            ]
            return

        self._mouse_buttons = [
            bool(buttons & MOUSE_LEFT_MASK),
            bool(buttons & MOUSE_MIDDLE_MASK),
            bool(buttons & MOUSE_RIGHT_MASK),
        ]
    
    def key_pressed(self, keystroke):
        """
        Handle key presses.
        
        Args:
            keystroke: The key that was pressed
            
        Returns:
            bool: True if the key was handled
        """
        key = keystroke.get_key()
        self._pressed_keys[key] = True
        
        if key == WorldInput.KEY_TAB:
            self.world.select_next_level()
            return True
        elif key == WorldInput.KEY_ENTER:
            self.world.run_selected()
            return True
        
        return False
    
    def key_released(self, keystroke):
        """
        Handle key releases.
        
        Args:
            keystroke: The key that was released
            
        Returns:
            bool: True if the key was handled
        """
        key = keystroke.get_key()
        if key in self._pressed_keys:
            self._pressed_keys[key] = False
        return False
    
    def mouse_event(self, mouse_stroke):
        """
        Handle mouse events.
        
        Args:
            mouse_stroke: The mouse event
            
        Returns:
            bool: True if the event was handled
        """
        from gengine.log import log_debug
        
        # Update mouse state
        self._mouse_loc = mouse_stroke.get_loc()
        # log_debug(f"Mouse event at {mouse_stroke.get_loc()}, button: {mouse_stroke.button}")
        
        if mouse_stroke.is_button():
            if mouse_stroke.is_left():
                self._mouse_buttons[0] = True
                log_debug(f"Left button click detected at {mouse_stroke.get_loc()}")
                # Force a run_selected call even if not directly over a level node
                self.world.run_selected()
                return True
            elif mouse_stroke.is_middle():
                self._mouse_buttons[1] = True
            elif mouse_stroke.is_right():
                self._mouse_buttons[2] = True
        
        return False
    
    def mouse_released(self, mouse_stroke):
        """
        Handle mouse releases.
        
        Args:
            mouse_stroke: The mouse event
            
        Returns:
            bool: True if the event was handled
        """
        if mouse_stroke.is_left():
            self._mouse_buttons[0] = False
        elif mouse_stroke.is_middle():
            self._mouse_buttons[1] = False
        elif mouse_stroke.is_right():
            self._mouse_buttons[2] = False
        return False
    
    def is_pressed(self, key):
        """
        Check if a key is pressed.
        
        Args:
            key (int): The key code
            
        Returns:
            bool: True if the key is pressed
        """
        return self._pressed_keys.get(key, False)
    
    def is_left_pressed(self):
        """
        Check if the left mouse button is pressed.
        
        Returns:
            bool: True if the left mouse button is pressed
        """
        return self._mouse_buttons[0]
    
    def is_middle_pressed(self):
        """
        Check if the middle mouse button is pressed.
        
        Returns:
            bool: True if the middle mouse button is pressed
        """
        return self._mouse_buttons[1]
    
    def is_right_pressed(self):
        """
        Check if the right mouse button is pressed.
        
        Returns:
            bool: True if the right mouse button is pressed
        """
        return self._mouse_buttons[2]
    
    def get_mouse_loc(self):
        """
        Get the mouse location.
        
        Returns:
            V2: The mouse location
        """
        return self._mouse_loc
    
    def to_string(self):
        """
        Get a string representation of the input state.
        
        Returns:
            str: A string representation
        """
        from gengine.v2 import V2
        mouse_pos = self.get_mouse_loc()
        return f"WorldInputProvider[mouse={mouse_pos}, left={self.is_left_pressed()}, middle={self.is_middle_pressed()}, right={self.is_right_pressed()}]"
