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

from gengine.no_copy import NoCopy
from gengine.v2 import V2
from gengine.ex_info import ExInfo
from level.layout_exception import LayoutException

class Shape(NoCopy):
    """
    Stores model shape.
    Used by MarkMask to check Field under shape.
    """
    
    def __init__(self, shape_str):
        """
        Read shape in format:
        "XXX...\\n"
        ".XXXXX\\n"
        "XX...X\\n"
        
        NOTE: rows do not need to have the same length
        
        Args:
            shape_str (str): String representation of the shape
            
        Raises:
            LayoutException: When shape has bad format
        """
        self.m_marks = []
        self.m_w = 0
        self.m_h = 0
        
        x = 0
        y = 0
        max_x = -1
        max_y = -1
        
        for i in range(len(shape_str)):
            char = shape_str[i]
            if char == '\n':
                y += 1
                x = 0
            elif char == 'X':
                self.m_marks.append(V2(x, y))
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                x += 1
            elif char == '.':
                x += 1
            else:
                raise LayoutException(ExInfo("bad shape char")
                    .add_info("char", char)
                    .add_info("shape", shape_str))
        
        self.m_w = max_x + 1
        self.m_h = max_y + 1
    
    def get_rel_locs(self):
        """
        Get all marks (relative locations) that make up this shape.
        
        Returns:
            list: List of V2 coordinates
        """
        return self.m_marks
    
    def get_w(self):
        """
        Get the width of the shape.
        
        Returns:
            int: Width of the shape
        """
        return self.m_w
    
    def get_h(self):
        """
        Get the height of the shape.
        
        Returns:
            int: Height of the shape
        """
        return self.m_h
    
    def __str__(self):
        """
        Get string representation of this shape.
        
        Returns:
            str: String representation of the shape's marks
        """
        result = ""
        for mark in self.m_marks:
            result += str(mark) + " "
        return result