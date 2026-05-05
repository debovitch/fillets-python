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
Debug console input handler.
"""

import pygame
from gengine.key_stroke import KeyStroke
from plan.state_input import StateInput

class ConsoleInput(StateInput):
    """Input handler for the debug console."""
    
    # Key constants
    KEY_HISTORY = 101
    KEY_BACKSPACE = 102
    KEY_CLEAR = 103
    KEY_ENTER = 104
    
    def __init__(self, console):
        """
        Initialize a new console input handler.
        
        Args:
            console (KeyConsole): The console to handle input for
        """
        StateInput.__init__(self, console)
        self.history = ""
        
        # Register key bindings
        self.keymap.register_key(KeyStroke(pygame.K_UP, 0), self._key_desc(self.KEY_HISTORY, "input history"))
        self.keymap.register_key(KeyStroke(pygame.K_BACKSPACE, 0), self._key_desc(self.KEY_BACKSPACE, "backspace"))
        self.keymap.register_key(KeyStroke(pygame.K_u, pygame.KMOD_CTRL), self._key_desc(self.KEY_CLEAR, "clear"))
        self.keymap.register_key(KeyStroke(pygame.K_RETURN, 0), self._key_desc(self.KEY_ENTER, "enter"))
    
    def get_console(self):
        """
        Get the console being handled.
        
        Returns:
            KeyConsole: The console
        """
        return self.state
    
    def enable_console(self):
        """Toggle the console."""
        self.quit_state()
    
    def enable_subtitles(self):
        """Enable subtitles (no-op)."""
        pass
    
    def spec_key(self, key_index):
        """
        Handle a special key press.
        
        Args:
            key_index (int): The index of the key pressed
        """
        if key_index == self.KEY_HISTORY:
            self.get_console().set_input(self.history)
        
        elif key_index == self.KEY_BACKSPACE:
            input_text = self.get_console().get_input()
            if input_text:
                input_text = input_text[:-1]
                self.get_console().set_input(input_text)
        
        elif key_index == self.KEY_CLEAR:
            self.get_console().set_input("")
        
        elif key_index == self.KEY_ENTER:
            input_text = self.get_console().get_input()
            if input_text:
                if self.get_console().send_command():
                    self.history = input_text
                    self.get_console().set_input("")
            else:
                self.quit_state()
        
        else:
            # Handle other keys using parent class
            StateInput.spec_key(self, key_index)
    
    def spec_stroke(self, stroke):
        """
        Handle a keystroke that isn't mapped to a special function.
        
        Args:
            stroke (KeyStroke): The keystroke
        """
        # Get the printable character from the keystroke
        unicode_char = stroke.get_unicode()
        if unicode_char and unicode_char.isprintable():
            input_text = self.get_console().get_input() + unicode_char
            self.get_console().set_input(input_text)