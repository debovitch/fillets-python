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
from gengine.agent.base_agent import BaseAgent, agent_class
from gengine.name import Name
from gengine.key_binder import KeyBinder
from gengine.key_stroke import KeyStroke
from gengine.mouse_stroke import MouseStroke
from gengine.v2 import V2
from gengine.input_handler import (
    MOUSE_LEFT_MASK,
    MOUSE_MIDDLE_MASK,
    MOUSE_RIGHT_MASK,
)
from gengine.agent.messager_agent import MessagerAgent
from gengine.message.simple_msg import SimpleMsg
from gengine.log import log_debug

@agent_class(Name.INPUT_NAME)
class InputAgent(BaseAgent):
    """
    Agent that handles input events and forwards them to input handlers.
    """
    
    def __init__(self):
        """
        Initialize the input agent.
        """
        super().__init__()
        self.key_state = {}  # Dictionary mapping key codes to boolean values
        self.key_binder = KeyBinder()
        self.handler = None
    
    def own_init(self):
        """
        Initialize input handling.
        Enable key repeat.
        """
        # Enable key repeat in pygame
        pygame.key.set_repeat(500, 30)  # Initial delay and interval in milliseconds
    
    def own_update(self):
        """
        Process input events and update the input handler.
        """
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Send a quit message to the application
                msg = SimpleMsg("app", "quit")
                MessagerAgent.agent().forward_new_msg(msg)
            
            elif event.type == pygame.KEYDOWN:
                # Handle key press
                self.key_state[event.key] = True
                handled = self.key_binder.key_down(event)
                if self.handler and not handled:
                    self.handler.key_event(KeyStroke(event))
            
            elif event.type == pygame.KEYUP:
                # Handle key release
                self.key_state[event.key] = False
                handled = self.key_binder.key_up(event)
                if self.handler and not handled:
                    self.handler.key_up(KeyStroke(event))
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse button press
                if self.handler:
                    # log_debug(f"Mouse down event: {event.button} at {event.pos}")
                    pos = self._screen_to_game_pos(event.pos)
                    self.handler.mouse_event(MouseStroke(event.button, pos[0], pos[1]))
                    
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     # Handle mouse button release
            #     if self.handler:
            #         log_debug(f"Mouse up event: {event.button} at {event.pos}")
            #         self.handler.mouse_released(MouseStroke(event))
        
        # Update the mouse state
        if self.handler:
            mouse_loc = self._get_mouse_pos()
            self.handler.mouse_state(V2(mouse_loc[0], mouse_loc[1]), self._get_mouse_state())
    
    def own_shutdown(self):
        """
        Clean up input handling.
        """
        # The key_binder will be cleaned up by Python's garbage collection
        pass
    
    def install_handler(self, handler):
        """
        Install a new input handler.
        
        Args:
            handler (InputHandler): The new input handler
        """
        if self.handler:
            self.handler.take_pressed(None)
            self.handler.mouse_state(V2(-1, -1), 0)
        
        self.handler = handler
        
        if self.handler:
            self.handler.take_pressed(self.key_state)
            mouse_loc = self._get_mouse_pos()
            self.handler.mouse_state(V2(mouse_loc[0], mouse_loc[1]), self._get_mouse_state())

    def _get_mouse_state(self):
        """Return a bit mask for the three primary mouse buttons."""
        buttons = pygame.mouse.get_pressed(3)
        mouse_state = 0
        if buttons[0]:
            mouse_state |= MOUSE_LEFT_MASK
        if buttons[1]:
            mouse_state |= MOUSE_MIDDLE_MASK
        if buttons[2]:
            mouse_state |= MOUSE_RIGHT_MASK
        return mouse_state
    
    def _get_mouse_pos(self):
        """Return mouse coordinates in logical game space."""
        from gengine.agent.video_agent import VideoAgent

        return VideoAgent.agent().get_mouse_pos()

    def _screen_to_game_pos(self, pos):
        """Convert display-space event coordinates to logical game space."""
        from gengine.agent.video_agent import VideoAgent

        return VideoAgent.agent().screen_to_game_pos(pos)

    def key_binder(self):
        """
        Get the key binder.
        
        Returns:
            KeyBinder: The key binder
        """
        return self.key_binder
    
