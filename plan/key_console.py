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
from gengine.key_stroke import KeyStroke
from gengine.mouse_stroke import MouseStroke

class KeyDesc:
    """
    Key description.
    Maps a key to a function and description.
    """
    
    def __init__(self, key, func, desc=""):
        """
        Initialize a key description.
        
        Args:
            key: The key code
            func: The function to call when the key is pressed
            desc: Description of the key function
        """
        self.key = key
        self.func = func
        self.desc = desc
    
    def get_key(self):
        """
        Get the key.
        
        Returns:
            int: The key code
        """
        return self.key
    
    def get_desc(self):
        """
        Get the description.
        
        Returns:
            str: The description
        """
        return self.desc
    
    def action(self):
        """Execute the key action."""
        self.func()

class KeyConsole(NoCopy):
    """
    Console for key input.
    Maps keys to actions.
    """
    
    def __init__(self):
        """Initialize a new key console."""
        self.keys = []
    
    def add_key(self, key, func, desc=""):
        """
        Add a key.
        
        Args:
            key: The key code
            func: The function to call when the key is pressed
            desc: Description of the key function
        """
        key_desc = KeyDesc(key, func, desc)
        self.keys.append(key_desc)
    
    def key_pressed(self, keystroke):
        """
        Handle key press.
        
        Args:
            keystroke: The key stroke
            
        Returns:
            bool: True if the key was handled
        """
        key = keystroke.get_key()
        
        for key_desc in self.keys:
            if key_desc.get_key() == key:
                key_desc.action()
                return True
        
        return False
    
    def mouse_event(self, stroke):
        """
        Handle mouse event.
        
        Args:
            stroke: The mouse stroke
            
        Returns:
            bool: True if the event was handled
        """
        # Console doesn't handle mouse events
        return False
    
    def get_help_text(self):
        """
        Get help text for this console.
        
        Returns:
            str: The help text
        """
        if not self.keys:
            return ""
        
        # Format key descriptions
        lines = []
        for key_desc in self.keys:
            desc = key_desc.get_desc()
            if desc:
                key_name = pygame.key.name(key_desc.get_key()).upper()
                lines.append(f"{key_name}: {desc}")
        
        return "\n".join(lines)