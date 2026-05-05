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

from gengine.no_copy import NoCopy

class ModelList(NoCopy):
    """
    Wrapper around a list of models.
    Provides convenience methods for operations on multiple models.
    """
    
    def __init__(self, models):
        """
        Create a new wrapper around a list of models.
        
        Args:
            models: The list of models to wrap
        """
        self.m_models = models
    
    def __iter__(self):
        """
        Allow iteration through models.
        
        Returns:
            iterator: An iterator through models
        """
        return iter(self.m_models)
    
    def __getitem__(self, index):
        """
        Get the model at the given index.
        
        Args:
            index: The index to get
            
        Returns:
            model: The model at the given index
        """
        return self.m_models[index]
    
    def __len__(self):
        """
        Get the number of models in the list.
        
        Returns:
            int: The number of models
        """
        return len(self.m_models)
    
    def size(self):
        """
        Get the number of models in the list.
        
        Returns:
            int: The number of models
        """
        return len(self.m_models)
    
    def draw_all_models(self, view):
        """
        Draw all models on the view.
        
        Args:
            view: The view to draw on
        """
        for model in self.m_models:
            if model:  # Check that model exists
                view.draw_model(model)
    
    def stone_on(self, slip):
        """
        Stone all models on fixed pad.
        
        Args:
            slip (Landslip): The landslip to use
            
        Returns:
            bool: True when a new model was stoned
        """
        change = False
        for model in self.m_models:
            if model and slip.stone_model(model):  # Check that model exists
                change = True
        return change
    
    def fall_on(self, slip):
        """
        Let all not stoned models fall.
        
        Args:
            slip (Landslip): The landslip to use
            
        Returns:
            bool: True when something is falling
        """
        falling = False
        for model in self.m_models:
            if model and slip.fall_model(model):  # Check that model exists
                falling = True
        return falling