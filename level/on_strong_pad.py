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


def _weight_value(weight):
    return weight.value if hasattr(weight, "value") else weight

class OnStrongPad(OnCondition):
    """
    Condition that checks if a model is on a strong pad (wall or powerful fish).
    """
    
    def __init__(self, weight):
        """
        Initialize a new OnStrongPad condition.
        
        Args:
            weight: The weight to check for
        """
        self.m_weight = weight
    
    def is_satisfy(self, model):
        """
        Check if the model is on a strong pad.
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the model is on a strong pad
        """
        return (model.is_wall() or
                (model.is_alive() and
                 _weight_value(model.get_power()) >= _weight_value(self.m_weight)))
    
    def is_wrong(self, model):
        """
        Check if the model is definitely not on a strong pad.
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the model is definitely not on a strong pad
        """
        return (model.is_alive() and
                _weight_value(model.get_power()) < _weight_value(self.m_weight))
