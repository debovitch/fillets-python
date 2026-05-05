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

class NoCopy:
    """
    Base class that prevents copying.
    
    In Python, we can achieve this by raising TypeError in the __copy__ 
    and __deepcopy__ methods, though Python doesn't prevent copying by default
    in the same way C++ does with private copy constructors.
    """
    
    def __copy__(self):
        """
        Prevent copying by raising an exception.
        
        Raises:
            TypeError: Always raises this error when copying is attempted
        """
        raise TypeError(f"{self.__class__.__name__} does not support copying")
    
    def __deepcopy__(self, memo):
        """
        Prevent deep copying by raising an exception.
        
        Args:
            memo: The memo dictionary for deepcopy
            
        Raises:
            TypeError: Always raises this error when deep copying is attempted
        """
        raise TypeError(f"{self.__class__.__name__} does not support deep copying")