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

import random

class Random:
    """
    Utility class for random number generation.
    """
    
    # Pre-generated random array used for deterministic random sequences
    _rand_array = bytearray(255)
    _initialized = False
    
    @classmethod
    def init(cls):
        """
        Initialize the random number generator.
        """
        if not cls._initialized:
            # Fill the array with random bytes
            for i in range(255):
                cls._rand_array[i] = random.randint(0, 255)
            cls._initialized = True
    
    @classmethod
    def random_int(cls, bound):
        """
        Generate a random integer between 0 (inclusive) and bound (exclusive).
        
        Args:
            bound (int): The upper bound (exclusive)
            
        Returns:
            int: A random integer between 0 and bound-1
        """
        return random.randint(0, bound-1)
    
    @classmethod
    def random_real(cls, bound):
        """
        Generate a random float between 0 (inclusive) and bound (exclusive).
        
        Args:
            bound (float): The upper bound (exclusive)
            
        Returns:
            float: A random float between 0 and bound
        """
        return random.random() * bound
    
    @classmethod
    def a_byte(cls, index):
        """
        Get a deterministic "random" byte based on an index.
        
        Args:
            index (int): The index
            
        Returns:
            int: A byte value (0-255)
        """
        if not cls._initialized:
            cls.init()
        
        # Ensure the index is within bounds with modulo
        return cls._rand_array[index % 255]