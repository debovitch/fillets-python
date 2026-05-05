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

class StringTool:
    """
    String utilities.
    Most of these functions are built into Python strings, but this class
    provides a consistent interface with the original C++ code.
    """
    
    @staticmethod
    def read_int(text, ok=None):
        """
        Try to parse an integer from text.
        
        Args:
            text (str): The text to parse
            ok (list): Optional list with one boolean element that will be set to True/False
                      (simulating the C++ out parameter)
            
        Returns:
            int: The parsed integer or 0 if parsing failed
        """
        try:
            value = int(text)
            if ok is not None:
                ok[0] = True
            return value
        except ValueError:
            if ok is not None:
                ok[0] = False
            return 0
    
    @staticmethod
    def to_string(value):
        """
        Convert a value to string.
        
        Args:
            value: The value to convert
            
        Returns:
            str: The string representation of the value
        """
        return str(value)
    
    @staticmethod
    def starts_with(string, prefix):
        """
        Check if string starts with the given prefix.
        
        Args:
            string (str): The string to check
            prefix (str): The prefix to look for
            
        Returns:
            bool: True if string starts with prefix, False otherwise
        """
        return string.startswith(prefix)
    
    @staticmethod
    def replace(buffer, pattern, new_string):
        """
        Replace all occurrences of pattern in buffer with new_string.
        
        Args:
            buffer (str): The string to modify
            pattern (str): The pattern to replace
            new_string (str): The replacement string
            
        Returns:
            str: The modified string
        """
        return buffer.replace(pattern, new_string)
    
    @staticmethod
    def split(string, separator):
        """
        Split a string by separator.
        
        Args:
            string (str): The string to split
            separator (str): The separator character
            
        Returns:
            list: List of strings split by separator
        """
        return string.split(separator)
    
    @staticmethod
    def utf8_length(string):
        """
        Get the length of a UTF-8 string in characters.
        
        Args:
            string (str): The string to measure
            
        Returns:
            int: The length of the string in characters
        """
        return len(string)