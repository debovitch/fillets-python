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
Description of control key.
"""

class KeyDesc:
    """Describes a control key with an index and description."""
    
    def __init__(self, index, desc):
        """
        Create a new key description.
        
        Args:
            index (int): Key index, should be unique in one GameState
            desc (str): Text description
        """
        self.index = index
        self.desc = desc
    
    def get_index(self):
        """
        Get the key index.
        
        Returns:
            int: The key index
        """
        return self.index
    
    def get_desc(self):
        """
        Get the key description.
        
        Returns:
            str: The key description
        """
        return self.desc