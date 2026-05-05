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
Table of defined keys.
"""

import pygame
from gengine.key_stroke import KeyStroke
from plan.key_desc import KeyDesc

class Keymap:
    """Maps key strokes to key descriptions."""
    
    def __init__(self):
        """Initialize a new keymap."""
        self.keys = {}
    
    def register_key(self, stroke, desc):
        """
        Register a new key mapping.
        
        Args:
            stroke (KeyStroke): The keystroke to register
            desc (KeyDesc): The key description to associate with the keystroke
        """
        self.keys[stroke] = desc
    
    def index_pressed(self, stroke):
        """
        Return the index of the pressed key.
        
        Args:
            stroke (KeyStroke): The keystroke to look up
            
        Returns:
            int: The key index, or -1 if not found
        """
        if stroke in self.keys:
            return self.keys[stroke].get_index()
        return -1