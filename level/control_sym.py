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

class ControlSym:
    """
    Control symbols used to save game moves.
    Symbols must be printable characters as they are stored in saved moves as plain text.
    """
    
    # Standard control symbols
    SYM_NONE = '\0'   # No action
    SYM_UP = 'U'      # Move up
    SYM_DOWN = 'D'    # Move down
    SYM_LEFT = 'L'    # Move left
    SYM_RIGHT = 'R'   # Move right
    SYM_SWITCH = 'S'  # Switch active fish
    
    # Fish-specific moves
    SYM_SMALL_UP = 'u'     # Small fish up
    SYM_SMALL_DOWN = 'd'   # Small fish down
    SYM_SMALL_LEFT = 'l'   # Small fish left
    SYM_SMALL_RIGHT = 'r'  # Small fish right
    
    SYM_BIG_UP = 'U'       # Big fish up
    SYM_BIG_DOWN = 'D'     # Big fish down
    SYM_BIG_LEFT = 'L'     # Big fish left
    SYM_BIG_RIGHT = 'R'    # Big fish right
    
    # Fish indices
    IDX_SMALL = 0  # Index of small fish
    IDX_BIG = 1    # Index of big fish
    
    def __init__(self, up, down, left, right):
        """
        Initialize control symbols.
        
        Args:
            up (str): Symbol for moving up
            down (str): Symbol for moving down
            left (str): Symbol for moving left
            right (str): Symbol for moving right
        """
        self.up = up
        self.down = down
        self.left = left
        self.right = right
    
    def get_up(self):
        """
        Get the symbol for moving up.
        
        Returns:
            str: The symbol for moving up
        """
        return self.up
    
    def get_down(self):
        """
        Get the symbol for moving down.
        
        Returns:
            str: The symbol for moving down
        """
        return self.down
    
    def get_left(self):
        """
        Get the symbol for moving left.
        
        Returns:
            str: The symbol for moving left
        """
        return self.left
    
    def get_right(self):
        """
        Get the symbol for moving right.
        
        Returns:
            str: The symbol for moving right
        """
        return self.right
        
    @staticmethod
    def symbol_to_index(symbol):
        """
        Convert a move symbol to a fish index.
        
        Args:
            symbol (str): The move symbol
            
        Returns:
            int: The fish index or -1 if invalid
        """
        if symbol in [ControlSym.SYM_SMALL_UP, ControlSym.SYM_SMALL_DOWN, 
                     ControlSym.SYM_SMALL_LEFT, ControlSym.SYM_SMALL_RIGHT]:
            return ControlSym.IDX_SMALL
        elif symbol in [ControlSym.SYM_BIG_UP, ControlSym.SYM_BIG_DOWN, 
                       ControlSym.SYM_BIG_LEFT, ControlSym.SYM_BIG_RIGHT]:
            return ControlSym.IDX_BIG
        return -1
    
    @staticmethod
    def symbol_to_dir(symbol):
        """
        Convert a move symbol to a direction symbol.
        
        Args:
            symbol (str): The move symbol
            
        Returns:
            str: The direction symbol or SYM_NONE if invalid
        """
        if symbol in [ControlSym.SYM_SMALL_UP, ControlSym.SYM_BIG_UP]:
            return ControlSym.SYM_UP
        elif symbol in [ControlSym.SYM_SMALL_DOWN, ControlSym.SYM_BIG_DOWN]:
            return ControlSym.SYM_DOWN
        elif symbol in [ControlSym.SYM_SMALL_LEFT, ControlSym.SYM_BIG_LEFT]:
            return ControlSym.SYM_LEFT
        elif symbol in [ControlSym.SYM_SMALL_RIGHT, ControlSym.SYM_BIG_RIGHT]:
            return ControlSym.SYM_RIGHT
        return ControlSym.SYM_NONE