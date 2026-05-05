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
Multi-line paragraph widget.
Translated from WiPara.h and WiPara.cpp
"""

from widget.v_box import VBox
from widget.wi_label import WiLabel
from gengine.string_tool import StringTool

class WiPara(VBox):
    """
    Multi-line paragraph widget.
    Automatically splits text into multiple lines.
    """
    
    def __init__(self, text, font, color):
        """
        Initialize a new paragraph widget.
        
        Args:
            text: The paragraph text
            font: The font to use
            color: The text color
        """
        VBox.__init__(self)
        
        # Split text into lines
        space = " "
        lines = text.split('\n')
        
        # Create a label for each line
        for line in lines:
            if not line:
                line = space
            self.add_widget(WiLabel(line, font, color))