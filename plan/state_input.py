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

class StateInput(InputHandler):
    """
    Base input handler for game states.
    """
    
    def __init__(self, state):
        """
        Initialize a new state input handler.
        
        Args:
            state: The game state
        """
        super().__init__()
        self.state = state
        self.provider = StateInputProvider(state, self)
    
    def get_provider(self):
        """
        Get the input provider.
        
        Returns:
            InputProvider: The input provider
        """
        return self.provider
    
    def key_pressed(self, keystroke):
        """
        Handle key press.
        
        Args:
            keystroke: The key stroke
            
        Returns:
            bool: True if the key was handled
        """
        return self.provider.key_pressed(keystroke)

    def key_up(self, keystroke):
        """
        Handle key release.

        Args:
            keystroke: The key stroke

        Returns:
            bool: True if the key was handled
        """
        return self.provider.key_released(keystroke)
    
    def mouse_event(self, stroke):
        """
        Handle mouse event.
        
        Args:
            stroke: The mouse stroke
            
        Returns:
            bool: True if the event was handled
        """
        return self.provider.mouse_event(stroke)

    def mouse_state(self, loc, buttons):
        """Synchronize continuous mouse state with the state provider."""
        super().mouse_state(loc, buttons)
        self.provider.mouse_state(loc, buttons)
        
    def mouse_released(self, stroke):
        """
        Handle mouse button release.
        
        Args:
            stroke (MouseStroke): The mouse stroke
            
        Returns:
            bool: True if the event was handled
        """
        if hasattr(self.provider, 'mouse_released'):
            return self.provider.mouse_released(stroke)
        return False

    def enable_subtitles(self):
        """Toggle subtitles."""
        from gengine.agent.option_agent import OptionAgent

        options = OptionAgent.agent()
        subtitles = options.get_as_bool("subtitles", True)
        options.set_persistent("subtitles", "0" if subtitles else "1")

class StateInputProvider(InputProvider):
    """
    Input provider for game states.
    """
    
    def __init__(self, state, handler=None):
        """
        Initialize a new state input provider.
        
        Args:
            state: The game state
            handler: The input handler owning this provider
        """
        self.state = state
        self.handler = handler
        from gengine.agent.video_agent import VideoAgent
        pos = VideoAgent.agent().get_mouse_pos()
        self.mouse_loc = V2(pos[0], pos[1])
        self._pressed_keys = {}
        self._mouse_buttons = [False, False, False]  # left, middle, right
    
    def key_pressed(self, keystroke):
        """
        Handle key press.
        
        Args:
            keystroke: The key stroke
            
        Returns:
            bool: True if the key was handled
        """
        key = keystroke.get_key()
        self._pressed_keys[key] = True

        if key == pygame.K_ESCAPE:
            self.state.quit_state()
            return True
        
        if key == pygame.K_F1:
            self.enable_help()
            return True
        
        if key == pygame.K_F10:
            self.enable_menu()
            return True

        if key == pygame.K_F6:
            self.enable_subtitles()
            return True
        
        return False

    def key_released(self, keystroke):
        """
        Handle key release.

        Args:
            keystroke: The key stroke

        Returns:
            bool: True if the key was handled
        """
        self._pressed_keys[keystroke.get_key()] = False
        return False

    def mouse_state(self, loc, buttons):
        """Update continuous mouse position and pressed buttons."""
        self.mouse_loc = loc if hasattr(loc, "get_x") else V2(loc[0], loc[1])

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
    
    def mouse_event(self, stroke):
        """
        Handle mouse event.
        
        Args:
            stroke: The mouse stroke
            
        Returns:
            bool: True if the event was handled
        """
        self.mouse_loc = stroke.get_loc()
        
        # Update button state
        if stroke.is_button():
            if stroke.is_left():
                self._mouse_buttons[0] = True
            elif stroke.is_middle():
                self._mouse_buttons[1] = True
            elif stroke.is_right():
                self._mouse_buttons[2] = True
                
        return False
        
    def mouse_released(self, stroke):
        """
        Handle mouse button release.
        
        Args:
            stroke: The mouse stroke
            
        Returns:
            bool: True if the event was handled
        """
        # Update button state
        if stroke.is_left():
            self._mouse_buttons[0] = False
        elif stroke.is_middle():
            self._mouse_buttons[1] = False
        elif stroke.is_right():
            self._mouse_buttons[2] = False
            
        return False
    
    def get_mouse_loc(self):
        """
        Get the current mouse location.
        
        Returns:
            V2: The mouse location
        """
        return self.mouse_loc
    
    def enable_menu(self):
        """Enable menu."""
        if self.handler and hasattr(self.handler, "enable_menu"):
            self.handler.enable_menu()
    
    def enable_help(self):
        """Enable help."""
        if self.handler and hasattr(self.handler, "enable_help"):
            self.handler.enable_help()
    
    def enable_subtitles(self):
        """Enable subtitles."""
        if self.handler and hasattr(self.handler, "enable_subtitles"):
            self.handler.enable_subtitles()
        
    def is_pressed(self, key):
        """
        Check if a key is pressed.
        
        Args:
            key: The key code
            
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
        
    def to_string(self):
        """
        Get a string representation of this input provider.
        
        Returns:
            str: A string representation
        """
        buttons = []
        if self.is_left_pressed():
            buttons.append("left")
        if self.is_middle_pressed():
            buttons.append("middle")
        if self.is_right_pressed():
            buttons.append("right")
            
        return f"StateInputProvider[mouse={self.mouse_loc}, buttons={buttons}]"
