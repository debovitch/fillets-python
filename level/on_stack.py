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

from level.on_condition import OnCondition
from level.cube import Cube
from level.dir import Dir

class OnStack(OnCondition):
    """
    Condition that checks if a model is on a stack of objects that are on something fixed.
    """
    
    def is_satisfy(self, model):
        """
        Check if the model is on a stack.
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the model is on a stack
        """
        if not model.is_alive():
            rules = model.get_rules()
            return (rules.get_dir() == Dir.DIR_NO and
                    rules.is_on_strong_pad(Cube.Weight.LIGHT))
        return False
    
    def is_wrong(self, model):
        """
        Check if the model is definitely not on a stack.
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the model is definitely not on a stack
        """
        return model.is_alive()
