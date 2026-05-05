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

from typing import Optional, Dict, List
from gengine.resource.resource_pack import ResourcePack
from gengine.resource.dialog import Dialog
from gengine.agent.option_agent import OptionAgent
from gengine.ex_info import ExInfo
from gengine.log import log_debug, log_warning

class ResDialogPack(ResourcePack[Dialog]):
    """
    Multi-language dialogs pack.
    Manages dialogs in different languages.
    """
    
    def __init__(self):
        """
        Initialize a new dialog pack.
        """
        super().__init__()
    
    def get_name(self) -> str:
        """
        Get the name of this resource pack.
        
        Returns:
            str: The name of the resource pack
        """
        return "dialog_pack"
    
    def match_score(self, first: str, second: str) -> int:
        """
        Calculate a matching score between two language names.
        
        Args:
            first: The first language name
            second: The second language name
            
        Returns:
            int: The matching score (higher is better)
        """
        # Exact match
        if first == second:
            return 100
        
        # First part matches (e.g., 'cs' matches 'cs_CZ')
        if first.startswith(second) or second.startswith(first):
            return 50
        
        # No match
        return 0
    
    def find_dialog(self, name: str, lang: str) -> Optional[Dialog]:
        """
        Find a dialog with the given name in the specified language.
        
        Args:
            name: The dialog name
            lang: The language to search for
            
        Returns:
            Dialog: The dialog or None if not found
        """
        # Get all dialogs with this name
        if name not in self.resources:
            return None
        
        dialogs = self.resources[name]
        if not dialogs:
            return None
        
        # Find the best match by language
        best_score = -1
        best_dialog = None
        
        for dialog in dialogs:
            score = self.match_score(dialog.get_lang(), lang)
            if score > best_score:
                best_score = score
                best_dialog = dialog
        
        # If no match, fall back to the first dialog
        if best_dialog is None and dialogs:
            best_dialog = dialogs[0]
            
        return best_dialog
    
    def find_dialog_hard(self, name: str) -> Optional[Dialog]:
        """
        Find a dialog with the given name in the 'hard' language.
        
        Args:
            name: The dialog name
            
        Returns:
            Dialog: The dialog or None if not found
        """
        # Use the current UI language, falling back to the default language.
        lang = OptionAgent.agent().get_param("lang", Dialog.DEFAULT_LANG)
        
        # Find the dialog
        return self.find_dialog(name, lang)
    
    def find_dialog_speech(self, name: str) -> Optional[Dialog]:
        """
        Find a dialog with the given name in the 'speech' language.
        
        Args:
            name: The dialog name
            
        Returns:
            Dialog: The dialog or None if not found
        """
        # Use the speech language when set, otherwise follow the UI language.
        lang = OptionAgent.agent().get_param(
            "speech", OptionAgent.agent().get_param("lang", Dialog.DEFAULT_LANG))
        
        # Find the dialog
        return self.find_dialog(name, lang)
    
    def unload_res(self, res: Dialog) -> None:
        """
        Free the given resource.
        
        Args:
            res: The resource to free
        """
        # Dialog objects will be freed by Python's garbage collector
        # The sound resources they use are managed by the sound system
        pass
