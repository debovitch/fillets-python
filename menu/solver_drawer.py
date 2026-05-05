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
Draws the best solver information.
Translated from SolverDrawer.h and SolverDrawer.cpp
"""

from gengine.log import log_warning
from gengine.path import Path
from widget.v_box import VBox
from effect.font import Font
from widget.labels import Labels
from widget.wi_para import WiPara
from gengine.string_tool import StringTool

class SolverDrawer(VBox):
    """
    Draws the best solver information in the level selection screen.
    Shows if the player's solution is better, equal or worse than the best recorded solution.
    """
    
    def __init__(self, status):
        """
        Prepare to draw info about best solver.
        
        Args:
            status: Shared level status
        """
        VBox.__init__(self)
        
        try:
            used_font = Font(Path.data_read_path("font/font_menu.ttf"), 14)
            used_color = (255, 255, 255, 255)
            
            labels = Labels(Path.data_read_path("script/labels.lua"))
            
            # Choose label based on comparison to best
            comparison = status.compare_to_best()
            if comparison > 0:
                label_name = "solver_better"
            elif comparison == 0:
                label_name = "solver_equals"
            else:
                label_name = "solver_worse"
            
            # Set up arguments for the label
            args = ["", str(status.get_best_moves()), status.get_best_author()]
            
            # Create paragraph widget
            para = WiPara(
                labels.get_formated_label(label_name, args),
                used_font, used_color
            )
            para.enable_centered()
            para.recenter()
            self.add_widget(para)
            
        except Exception as e:
            log_warning(f"Failed to create solver drawer: {e}")