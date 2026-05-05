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

from gengine.resource.dialog import Dialog

class LevelDesc:
    """
    Multi-language level description.
    """
    
    def __init__(self, codename=None, level_name=None, desc=None):
        """
        Initialize an empty level description collection or with an initial item.
        
        Args:
            codename: The level code name (optional)
            level_name: The display name of the level (optional)
            desc: The description text (optional)
        """
        self.descriptions = {}
        
        # Add initial description if provided
        if codename is not None and level_name is not None and desc is not None:
            self.add_desc(codename, level_name, desc)
    
    def add_desc(self, codename, level_name, desc):
        """
        Add a description for a level.
        
        Args:
            codename: The level code name
            level_name: The display name of the level
            desc: The description text
        """
        self.descriptions[codename] = {"name": level_name, "desc": desc}
    
    def find_desc(self, codename):
        """
        Find a description by code name.
        
        Args:
            codename: The level code name
            
        Returns:
            dict: The level description or None if not found
        """
        return self.descriptions.get(codename)
    
    def find_level_name(self, codename):
        """
        Find a level name by code name.
        
        Args:
            codename: The level code name
            
        Returns:
            str: The level name or None if not found
        """
        desc = self.descriptions.get(codename)
        if desc:
            return desc["name"]
        return None
        
    def get_lang(self):
        """
        Get the language code.
        
        Returns:
            str: The language code, empty for base class
        """
        return ""
        
    def get_desc(self):
        """
        Get the description text.
        
        Returns:
            str: The description text, empty for base class
        """
        return ""
        
    def get_level_name(self):
        """
        Get the level name.
        
        Returns:
            str: The level name, empty for base class
        """
        return ""


class LevelDescItem(Dialog):
    """
    Multi-language level description item.
    """
    
    def __init__(self, lang: str, level_name: str, desc: str):
        """
        Initialize a level description.
        
        Args:
            lang: The language code
            level_name: The name of the level
            desc: The description text
        """
        super().__init__(lang, "", desc)
        self.level_name = level_name
    
    def get_level_name(self) -> str:
        """
        Get the level name.
        
        Returns:
            str: The level name
        """
        return self.level_name
    
    def get_desc(self) -> str:
        """
        Get the level description.
        
        Returns:
            str: The level description
        """
        return self.get_subtitle()