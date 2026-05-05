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

class KeyStroke:
    """
    Represents a keyboard keystroke with modifiers.
    """
    
    # Modifier flags to pay attention to (CTRL and ALT)
    STROKE_IGNORE = ~(pygame.KMOD_CTRL | pygame.KMOD_ALT)
    
    def __init__(self, keysym_or_key, mod=None, unicode=None):
        """
        Initialize a new keystroke.
        
        Args:
            keysym_or_key: Either a pygame event or a key constant
            mod (int, optional): Modifier flags
            unicode (str, optional): Unicode character
        """
        if isinstance(keysym_or_key, pygame.event.Event):
            # Extract from pygame event
            self.sym = keysym_or_key.key
            self.mod = self.mod_strip(keysym_or_key.mod)
            self.unicode = keysym_or_key.unicode if hasattr(keysym_or_key, 'unicode') else ""
        else:
            # Extract from parameters
            self.sym = keysym_or_key
            self.mod = self.mod_strip(mod or 0)
            self.unicode = unicode or ""
    
    @staticmethod
    def mod_strip(mod):
        """
        Strip out modifiers we don't care about.
        
        Args:
            mod (int): The modifier flags
            
        Returns:
            int: The stripped modifier flags
        """
        return mod & ~KeyStroke.STROKE_IGNORE
    
    def get_key(self):
        """
        Get the key code.
        
        Returns:
            int: The key code
        """
        return self.sym
    
    def get_unicode(self):
        """
        Get the Unicode character.
        
        Returns:
            str: The Unicode character
        """
        return self.unicode
    
    def less(self, other):
        """
        Compare this keystroke with another.
        
        Args:
            other (KeyStroke): The other keystroke
            
        Returns:
            bool: True if this keystroke is less than the other
        """
        if self.sym < other.sym:
            return True
        if self.sym > other.sym:
            return False
        return self.mod < other.mod
    
    def equals(self, other):
        """
        Check if this keystroke equals another.
        
        Args:
            other (KeyStroke): The other keystroke
            
        Returns:
            bool: True if the keystrokes are equal
        """
        return self.sym == other.sym and self.mod == other.mod
    
    def __eq__(self, other):
        """
        Check if this keystroke equals another using the == operator.
        
        Args:
            other (KeyStroke): The other keystroke
            
        Returns:
            bool: True if the keystrokes are equal
        """
        if not isinstance(other, KeyStroke):
            return False
        return self.equals(other)
    
    def __lt__(self, other):
        """
        Check if this keystroke is less than another using the < operator.
        
        Args:
            other (KeyStroke): The other keystroke
            
        Returns:
            bool: True if this keystroke is less than the other
        """
        if not isinstance(other, KeyStroke):
            return NotImplemented
        return self.less(other)
    
    def __hash__(self):
        """
        Get the hash code for this keystroke.
        
        Returns:
            int: The hash code
        """
        return hash((self.sym, self.mod))
    
    def to_string(self):
        """
        Get a string representation of this keystroke.
        
        Returns:
            str: A string representation
        """
        key_name = pygame.key.name(self.sym)
        mod_str = ""
        
        if self.mod & pygame.KMOD_CTRL:
            mod_str += "CTRL+"
        if self.mod & pygame.KMOD_ALT:
            mod_str += "ALT+"
        
        return f"{mod_str}{key_name.upper()}"
    
    def __str__(self):
        """
        Get a string representation of this keystroke.
        
        Returns:
            str: A string representation
        """
        return self.to_string()