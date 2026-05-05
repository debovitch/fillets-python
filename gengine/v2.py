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

from gengine.string_tool import StringTool

class V2:
    """
    2D vector class for positions and offsets.
    Represents a point (x, y) in 2D space.
    """
    
    def __init__(self, x, y):
        """
        Initialize a new 2D vector.
        
        Args:
            x (int): The x-coordinate
            y (int): The y-coordinate
        """
        self.x = x
        self.y = y
    
    def get_x(self):
        """
        Get the x-coordinate.
        
        Returns:
            int: The x-coordinate
        """
        return self.x
    
    def get_y(self):
        """
        Get the y-coordinate.
        
        Returns:
            int: The y-coordinate
        """
        return self.y
    
    def plus(self, other, y=None):
        """
        Add another vector or an (x, y) pair to this one.
        
        Args:
            other (V2|int): The vector or x-coordinate to add
            y (int): Optional y-coordinate to add
            
        Returns:
            V2: A new vector representing the sum
        """
        if y is not None:
            return V2(self.x + other, self.y + y)
        return V2(self.x + other.x, self.y + other.y)
    
    def minus(self, other):
        """
        Subtract another vector from this one.
        
        Args:
            other (V2): The vector to subtract
            
        Returns:
            V2: A new vector representing the difference
        """
        return V2(self.x - other.x, self.y - other.y)
    
    def scale(self, rate):
        """
        Scale the vector by a factor.
        
        Args:
            rate (int): The scaling factor
            
        Returns:
            V2: A new scaled vector
        """
        return V2(self.x * rate, self.y * rate)
    
    def shrink(self, rate):
        """
        Shrink the vector by dividing by a factor.
        
        Args:
            rate (int): The division factor (must not be zero)
            
        Returns:
            V2: A new shrunk vector
            
        Raises:
            AssertionError: If rate is zero
        """
        assert rate != 0, "Division by zero"
        return V2(self.x // rate, self.y // rate)
    
    def equals(self, other):
        """
        Check if this vector equals another.
        
        Args:
            other (V2): The vector to compare with
            
        Returns:
            bool: True if vectors are equal, False otherwise
        """
        return self.x == other.x and self.y == other.y
    
    def __eq__(self, other):
        """
        Check if this vector equals another using == operator.
        
        Args:
            other (V2): The vector to compare with
            
        Returns:
            bool: True if vectors are equal, False otherwise
        """
        if not isinstance(other, V2):
            return False
        return self.equals(other)
    
    def __str__(self):
        """
        Get string representation of this vector.
        
        Returns:
            str: String representation in format [x,y]
        """
        return f"[{self.x},{self.y}]"
        
    def to_string(self):
        """
        Get string representation of this vector (alias for __str__).
        
        Returns:
            str: String representation in format [x,y]
        """
        return self.__str__()
