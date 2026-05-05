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

from gengine.path import Path
from gengine.script.scripter import Scripter
from widget.v_box import VBox
from widget.h_box import HBox
from widget.radio_box import RadioBox

class SelectLang(VBox, Scripter):
    """
    Menu with flags to select preferred language.
    """
    
    # Maximum width for a row of flags
    MAX_WIDTH = 200
    
    def __init__(self, option, datafile):
        """
        Initialize language selector.
        
        Args:
            option (str): Option name
            datafile (Path): Script file with language options
        """
        VBox.__init__(self)
        Scripter.__init__(self)
        
        self.option = option
        self.active_row = HBox()
        
        # Register script function
        self.script.register_func("select_addFlag", self.script_add_flag)
        
        # Include script file
        self.script_include(datafile)
        
        # Add the final row if it's not empty
        if self.active_row.widgets:
            self.add_widget(self.active_row)
    
    def add_flag(self, value, picture):
        """
        Add a flag to the selector.
        
        Args:
            value (str): Language value
            picture (Path): Flag picture path
        """
        flag = RadioBox(self.option, value, picture)
        flag.set_tip(value)
        self.active_row.add_widget(flag)
        
        # If the row is full, start a new row
        if self.active_row.get_w() > self.MAX_WIDTH:
            self.add_widget(self.active_row)
            self.active_row = HBox()
    
    def script_add_flag(self, args):
        """
        Script function to add a flag.
        
        Args:
            args: Script arguments (value, picture)
            
        Returns:
            list: Empty list
        """
        value = args[0]
        picture = args[1]
        
        self.add_flag(value, Path.data_read_path(picture))
        return []