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

class LevelInput(InputHandler):
    """
    Input handler for the level.
    Handles keyboard and mouse input for the level.
    """
    
    def __init__(self, level):
        """
        Initialize level input.
        
        Args:
            level: The level this input handler belongs to
        """
        InputHandler.__init__(self)
        self.level = level
        self.provider = InputProviderImpl(level)
    
    def get_provider(self):
        """
        Get the input provider.
        
        Returns:
            InputProvider: The input provider
        """
        return self.provider
    
    def key_pressed(self, keystroke):
        """
        Handle a key press.
        
        Args:
            keystroke: The key that was pressed
            
        Returns:
            bool: True if the key was handled
        """
        return self.provider.key_pressed(keystroke)
    
    def mouse_event(self, mouse_stroke):
        """
        Handle a mouse event.
        
        Args:
            mouse_stroke: The mouse event
            
        Returns:
            bool: True if the event was handled
        """
        return self.provider.mouse_event(mouse_stroke)

    def key_up(self, keystroke):
        """
        Handle a key release.

        Args:
            keystroke: The key that was released

        Returns:
            bool: True if the key was handled
        """
        return self.provider.key_released(keystroke)

    def mouse_state(self, loc, buttons):
        """Synchronize continuous mouse state with the level provider."""
        super().mouse_state(loc, buttons)
        self.provider.mouse_state(loc, buttons)

class InputProviderImpl(InputProvider):
    """Input provider implementation for the level."""
    
    def __init__(self, level):
        """
        Initialize the input provider.
        
        Args:
            level: The level this input provider belongs to
        """
        self.level = level
        self._pressed_keys = {}
        self._mouse_buttons = [False, False, False]  # left, middle, right
        self._mouse_loc = None
        import pygame
        self._mouse_loc = pygame.mouse.get_pos()

    def mouse_state(self, loc, buttons):
        """Update continuous mouse position and pressed buttons."""
        self._mouse_loc = loc

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
        Handle a key press.
        
        Args:
            keystroke: The key that was pressed
            
        Returns:
            bool: True if the key was handled
        """
        # Store key state
        key = keystroke.get_key()
        self._pressed_keys[key] = True

        if key == pygame.K_ESCAPE:
            self.level.quit_state()
            return True

        if key == pygame.K_F1:
            from option.menu_help import MenuHelp
            self.level.push_state(MenuHelp())
            return True

        if key == pygame.K_F10:
            from option.menu_options import MenuOptions
            self.level.push_state(MenuOptions())
            return True

        if key == pygame.K_F2:
            if not self.level.is_acting():
                self.level.action_save()
            return True

        if key == pygame.K_F3:
            if not self.level.is_showing():
                self.level.action_load()
            return True

        if key == pygame.K_F6:
            from gengine.agent.option_agent import OptionAgent
            options = OptionAgent.agent()
            subtitles = options.get_as_bool("subtitles", True)
            options.set_persistent("subtitles", "0" if subtitles else "1")
            return True

        if key == pygame.K_F5:
            from gengine.agent.option_agent import OptionAgent
            options = OptionAgent.agent()
            show_steps = options.get_as_bool("show_steps", True)
            options.set_persistent("show_steps", "0" if show_steps else "1")
            return True

        if key == pygame.K_BACKSPACE:
            self.level.interrupt_show()
            self.level.action_restart(1)
            return True

        if key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            if not self.level.is_showing():
                self.level.action_undo(1)
            return True

        if key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            if not self.level.is_showing():
                self.level.action_undo(-1)
            return True

        if key == pygame.K_SPACE:
            if not self.level.is_acting():
                self.level.switch_fish()
            return True
        
        self.level.control_event(keystroke)
        return True
    
    def key_released(self, keystroke):
        """
        Handle a key release.
        
        Args:
            keystroke: The key that was released
            
        Returns:
            bool: True if the key was handled
        """
        # Update key state
        key = keystroke.get_key()
        if key in self._pressed_keys:
            self._pressed_keys[key] = False

        if key in (pygame.K_MINUS, pygame.K_KP_MINUS,
                   pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            self.level.action_undo_finish()
            return True

        return True
    
    def mouse_event(self, mouse_stroke):
        """
        Handle a mouse event.
        
        Args:
            mouse_stroke: The mouse event
            
        Returns:
            bool: True if the event was handled
        """
        # Update mouse state
        self._mouse_loc = mouse_stroke.get_loc()
        
        if mouse_stroke.is_button():
            if mouse_stroke.is_left():
                self._mouse_buttons[0] = True
            elif mouse_stroke.is_middle():
                self._mouse_buttons[1] = True
            elif mouse_stroke.is_right():
                self._mouse_buttons[2] = True
                
            # Forward to level
            self.level.control_mouse(mouse_stroke)
        return True
    
    def mouse_released(self, mouse_stroke):
        """
        Handle a mouse release.
        
        Args:
            mouse_stroke: The mouse event
            
        Returns:
            bool: True if the event was handled
        """
        # Update mouse state
        if mouse_stroke.is_left():
            self._mouse_buttons[0] = False
        elif mouse_stroke.is_middle():
            self._mouse_buttons[1] = False
        elif mouse_stroke.is_right():
            self._mouse_buttons[2] = False
        return True
        
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
        loc = self._mouse_loc
        if hasattr(loc, "get_x"):
            return loc
        from gengine.v2 import V2
        return V2(loc[0], loc[1])
    
    def to_string(self):
        """
        Get a string representation of the input state.
        
        Returns:
            str: A string representation
        """
        from gengine.v2 import V2
        mouse_pos = self.get_mouse_loc()
        return f"InputProvider[mouse={mouse_pos}, left={self.is_left_pressed()}, middle={self.is_middle_pressed()}, right={self.is_right_pressed()}]"
