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

class ExInfo:
    """
    Detailed exception information.
    Used to build informative error messages with context information.
    """
    
    def __init__(self, problem):
        """
        Initialize with a problem description.
        
        Args:
            problem (str): Short description of the problem
        """
        self.what_str = problem
    
    def what(self):
        """
        Get the error message.
        
        Returns:
            str: The complete error message
        """
        return self.what_str
    
    def info(self):
        """
        Get the error information.
        
        Returns:
            str: The error information string
        """
        return self.what_str
    
    def add_info(self, name, value):
        """
        Add more contextual information to the error message.
        
        Args:
            name (str): The name/description of the value
            value: The value (str or number)
            
        Returns:
            ExInfo: self for method chaining
        """
        self.what_str += f"; {name}="
        
        # Handle different value types
        if isinstance(value, str):
            self.what_str += f"'{value}'"
        else:
            self.what_str += str(value)
            
        return self