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
from level.cube import Cube
from level.dir import Dir

class Landslip(NoCopy):
    """
    Landslip for every round.
    Handles the physics of falling objects.
    """
    
    def __init__(self, models):
        """
        Initialize a new landslip.
        
        Args:
            models: The list of models to check for falling
        """
        self.m_models = models
        self.m_impact = Cube.Weight.NONE
        
        # Initialize stoned array for all models
        if hasattr(models, '__len__'):
            self.m_stoned = [False] * len(models)
        else:
            # Fall back to a simple list if models is not a list
            self.m_stoned = []
    
    def compute_fall(self):
        """
        Identify falling objects.
        
        Returns:
            bool: whether something is falling
        """
        # Stone all objects that are fixed or on a pad
        changed = True
        while changed:
            changed = self.stone_all_models()
        
        # Apply falling to all objects that are not stoned
        return self.fall_all_models()
    
    def stone_all_models(self):
        """
        Stone all models that are fixed or on pads.
        
        Returns:
            bool: True if any model was newly stoned
        """
        changed = False
        for model in self.m_models:
            if model and self.stone_model(model):
                changed = True
        return changed
    
    def fall_all_models(self):
        """
        Apply falling to all unstoned models.
        
        Returns:
            bool: True if any model is falling
        """
        falling = False
        for model in self.m_models:
            if model and self.fall_model(model):
                falling = True
        return falling
    
    def stone_model(self, model):
        """
        Mark a model as stoned (stable, not falling).
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the model was newly stoned
        """
        change = False
        if not self.is_stoned(model):
            if self.is_fixed(model) or self.is_on_pad(model):
                self.stone(model)
                change = True
        return change
    
    def is_on_pad(self, model):
        """
        Check if the model is on a pad.
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the model is on a pad
        """
        if not model.get_rules():
            return False
            
        pad = model.get_rules().get_resist(Dir.DIR_DOWN)
        for pad_model in pad:
            if self.is_fixed(pad_model):
                return True
        return False
    
    def is_fixed(self, model):
        """
        Check if the model is fixed.
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the model is fixed
        """
        return (self.is_stoned(model) or 
                model.is_wall() or 
                model.is_alive() or 
                model.is_lost())
    
    def is_stoned(self, model):
        """
        Check if the model is stoned.
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the model is stoned
        """
        index = model.get_index()
        if index > -1 and index < len(self.m_stoned):
            return self.m_stoned[index]
        else:
            return True
    
    def stone(self, model):
        """
        Mark a model as stoned.
        
        Args:
            model: The model to stone
        """
        index = model.get_index()
        if index > -1:
            # Expand stoned array if needed
            while index >= len(self.m_stoned):
                self.m_stoned.append(False)
            self.m_stoned[index] = True
    
    def fall_model(self, model):
        """
        Let model fall.
        
        Args:
            model: The model to fall
            
        Returns:
            bool: True if the model is falling
        """
        falling = False
        if not self.is_fixed(model):
            model.get_rules().action_fall()
            falling = True
        else:
            if model.get_rules() and hasattr(model.get_rules(), 'clear_last_fall'):
                last_fall = model.get_rules().clear_last_fall()
                if last_fall and self.m_impact.value < model.get_weight().value:
                    self.m_impact = model.get_weight()
        return falling
    
    def get_impact(self):
        """
        Get the impact weight.
        
        Returns:
            Cube.Weight: The impact weight
        """
        return self.m_impact