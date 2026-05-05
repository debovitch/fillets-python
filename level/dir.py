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

from enum import Enum
from gengine.v2 import V2

class Dir(Enum):
    """
    Direction enumeration with conversion to coordinates.
    """
    DIR_NO = 0
    DIR_UP = 1
    DIR_DOWN = 2
    DIR_LEFT = 3
    DIR_RIGHT = 4
    
    @staticmethod
    def dir2xy(direction):
        """
        Convert a direction to relative coordinates.
        
        Args:
            direction (Dir): The direction to convert
            
        Returns:
            V2: The relative coordinates for the direction
            
        Raises:
            AssertionError: If the direction is unknown
        """
        if direction == Dir.DIR_UP:
            return V2(0, -1)
        elif direction == Dir.DIR_DOWN:
            return V2(0, 1)
        elif direction == Dir.DIR_LEFT:
            return V2(-1, 0)
        elif direction == Dir.DIR_RIGHT:
            return V2(1, 0)
        elif direction == Dir.DIR_NO:
            return V2(0, 0)
        else:
            assert False, "Unknown direction"