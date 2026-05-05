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
Base exception class.
"""

class BaseException(Exception):
    """
    Base exception with detailed information.
    All game exceptions should inherit from this class.
    """
    
    def __init__(self, info):
        """
        Initialize a base exception.
        
        Args:
            info (ExInfo): Information about the exception
        """
        Exception.__init__(self, info.info())
        self.m_info = info
    
    def info(self):
        """
        Get the exception information.
        
        Returns:
            ExInfo: The exception information
        """
        return self.m_info