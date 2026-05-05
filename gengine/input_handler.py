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
from gengine.no_copy import NoCopy
from gengine.input_provider import InputProvider
from gengine.v2 import V2
from gengine.ex_info import ExInfo

MOUSE_LEFT_MASK = 1 << 0
MOUSE_MIDDLE_MASK = 1 << 1
MOUSE_RIGHT_MASK = 1 << 2


class InputHandler(InputProvider, NoCopy):
    """
    Handle input events.
    Events:
    - key_event() is called when a new key is pressed.
    - mouse_event() is called when there is a mouse click.
    - mouse_state() is called every cycle to update mouse position.
    
    Pressed keys are stored in key_state dictionary, which is shared
    and updated by InputAgent.
    """
    
    def __init__(self):
        """
        Initialize a new input handler.
        """
        self.key_state = None
        self.buttons = 0
        self.mouse_loc = V2(-1, -1)
    
    def take_pressed(self, key_state):
        """
        Set the key state dictionary.
        
        Args:
            key_state (dict): The key state dictionary mapping key codes to boolean values
        """
        self.key_state = key_state
    
    def mouse_state(self, loc, buttons):
        """
        Update the mouse state.
        
        Args:
            loc (V2): The mouse location
            buttons (int): The button state
        """
        self.mouse_loc = loc
        self.buttons = buttons
    
    def key_event(self, stroke):
        """
        Handle a key press event.
        
        Args:
            stroke (KeyStroke): The key stroke
        """
        from gengine.log import log_debug
        # log_debug(f"Key event: {stroke}")
        
        # Default behavior should be to call key_pressed on handler classes that implement it
        if hasattr(self, 'key_pressed'):
            return self.key_pressed(stroke)
            
        return False
    
    def key_up(self, stroke):
        """
        Handle a key release event.
        
        Args:
            stroke (KeyStroke): The key stroke
        """
        pass
    
    def mouse_event(self, buttons):
        """
        Handle a mouse button event.
        
        Args:
            buttons (MouseStroke): The mouse stroke
        """
        # log_debug(f"Mouse event in handler: {buttons.button} at {buttons.get_loc()}")
        return False
    
    def is_pressed(self, key):
        """
        Check if a key is pressed.
        
        Args:
            key (int): The key code
            
        Returns:
            bool: True if the key is pressed
        """
        return self.key_state is not None and self.key_state.get(key, False)
    
    def is_left_pressed(self):
        """
        Check if the left mouse button is pressed.
        
        Returns:
            bool: True if the left mouse button is pressed
        """
        return bool(self.buttons & MOUSE_LEFT_MASK)
    
    def is_middle_pressed(self):
        """
        Check if the middle mouse button is pressed.
        
        Returns:
            bool: True if the middle mouse button is pressed
        """
        return bool(self.buttons & MOUSE_MIDDLE_MASK)
    
    def is_right_pressed(self):
        """
        Check if the right mouse button is pressed.
        
        Returns:
            bool: True if the right mouse button is pressed
        """
        return bool(self.buttons & MOUSE_RIGHT_MASK)
    
    def get_mouse_loc(self):
        """
        Get the mouse location.
        
        Returns:
            V2: The mouse location
        """
        return self.mouse_loc
    
    def to_string(self):
        """
        Get a string representation of the input state.
        
        Returns:
            str: A string representation
        """
        return ExInfo("input").add_info("mouse", str(self.mouse_loc)).add_info("buttons", self.buttons).info()
