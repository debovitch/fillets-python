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
Loads localized labels.
Translated from Labels.h and Labels.cpp
"""

from gengine.resource.res_dialog_pack import ResDialogPack
from gengine.resource.dialog import Dialog
from gengine.script.scripter import Scripter
from gengine.string_tool import StringTool

class Labels(Scripter):
    """
    Loads localized labels from Lua scripts.
    Provides access to localized text strings.
    """
    
    def __init__(self, source):
        """
        Initialize labels from a source file.
        
        Args:
            source: Path to the source Lua file
        """
        Scripter.__init__(self)
        
        self.labels = ResDialogPack()
        
        # Register Lua functions
        self.script.state.globals()["label_text"] = self._label_text
        
        # Load the script
        self.script_include(source)
    
    def __del__(self):
        """Clean up resources."""
        if hasattr(self, 'labels') and self.labels:
            self.labels.remove_all()
    
    def _label_text(self, label_name, lang, text):
        """
        Lua callback to add a label.
        
        Args:
            label_name: The label name
            lang: The language code
            text: The label text
        """
        self.add_label(label_name, lang, text)
        return True
    
    def add_label(self, name, lang, text):
        """
        Add a label.
        
        Args:
            name: The label name
            lang: The language code
            text: The label text
        """
        self.labels.add_res(name, Dialog(lang, "", text))
    
    def get_label(self, name):
        """
        Get a label by name.
        
        Args:
            name: The label name
            
        Returns:
            str: The label text or "???" if not found
        """
        dialog = self.labels.find_dialog_hard(name)
        if dialog:
            return dialog.get_subtitle()
        return "???"
    
    def get_formated_label(self, name, args):
        """
        Get a formatted label by name.
        
        Args:
            name: The label name
            args: The formatting arguments
            
        Returns:
            str: The formatted label text or "???" if not found
        """
        dialog = self.labels.find_dialog_hard(name)
        if dialog:
            return dialog.get_formated_subtitle(args)
        return "???"