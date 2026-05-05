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
from level.dir import Dir

class MarkMask(NoCopy):
    """
    Handles object presence on the field.
    Marks/unmasks an object's position on the field.
    """
    
    def __init__(self, model, field):
        """
        Initialize a new mark mask.
        
        Args:
            model: The model to mask
            field: The field to mask on
        """
        self.m_model = model
        self.m_field = field
        self.m_shape = model.get_shape() if hasattr(model, 'get_shape') else None
    
    def mask(self):
        """
        Mask the model on the field.
        """
        if not self.m_model.is_out():
            loc = self.m_model.get_location()
            if self.m_shape:
                for rel_loc in self.m_shape.get_rel_locs():
                    position = loc.plus(rel_loc)
                    self.m_field.set_model(position, self.m_model, None)
            else:
                # Simplified for when shape is not available
                self.m_field.set_model(loc, self.m_model, None)
    
    def unmask(self):
        """
        Unmask the model from the field.
        """
        if not self.m_model.is_out():
            loc = self.m_model.get_location()
            if self.m_shape:
                for rel_loc in self.m_shape.get_rel_locs():
                    position = loc.plus(rel_loc)
                    self.m_field.set_model(position, None, self.m_model)
            else:
                # Simplified for when shape is not available
                self.m_field.set_model(loc, None, self.m_model)
    
    def get_resist(self, dir):
        """
        Get models that resist movement in direction.
        
        Args:
            dir (Dir): The direction to check
            
        Returns:
            list: Models that resist movement
        """
        result = []
        if not self.m_model.is_out():
            loc = self.m_model.get_location()
            shift = Dir.dir2xy(dir)
            
            if self.m_shape:
                for rel_loc in self.m_shape.get_rel_locs():
                    position = loc.plus(rel_loc).plus(shift)
                    model = self.m_field.get_model(position)
                    if model and model != self.m_model:
                        # Add model to result if not already present
                        if model not in result:
                            result.append(model)
            else:
                # Simplified for when shape is not available
                position = loc.plus(shift)
                model = self.m_field.get_model(position)
                if model and model != self.m_model:
                    result.append(model)
        
        return result
    
    def get_placed_resist(self, loc):
        """
        Get models that would resist the model being placed at the given location.
        
        Args:
            loc: The location to check
            
        Returns:
            list: Models that would resist placement
        """
        result = []
        
        if self.m_shape:
            for rel_loc in self.m_shape.get_rel_locs():
                position = loc.plus(rel_loc)
                model = self.m_field.get_model(position)
                if model and model != self.m_model:
                    if model not in result:
                        result.append(model)
        else:
            # Simplified for when shape is not available
            model = self.m_field.get_model(loc)
            if model and model != self.m_model:
                result.append(model)
        
        return result
    
    def get_border_dir(self):
        """
        Get the direction the model is touching a border.
        
        Returns:
            Dir: The direction of the border, or DIR_NO if not at border
        """
        if not self.m_model.is_out():
            loc = self.m_model.get_location()
            w = self.m_field.get_w()
            h = self.m_field.get_h()
            
            # Check all parts of the shape
            if self.m_shape:
                for rel_loc in self.m_shape.get_rel_locs():
                    position = loc.plus(rel_loc)
                    x, y = position.get_x(), position.get_y()
                    
                    # Check if at border
                    if x <= 0:
                        return Dir.DIR_LEFT
                    elif x >= w - 1:
                        return Dir.DIR_RIGHT
                    elif y <= 0:
                        return Dir.DIR_UP
                    elif y >= h - 1:
                        return Dir.DIR_DOWN
            else:
                # Simplified for when shape is not available
                x, y = loc.get_x(), loc.get_y()
                if x <= 0:
                    return Dir.DIR_LEFT
                elif x >= w - 1:
                    return Dir.DIR_RIGHT
                elif y <= 0:
                    return Dir.DIR_UP
                elif y >= h - 1:
                    return Dir.DIR_DOWN
        
        return Dir.DIR_NO
    
    def is_fully_out(self):
        """
        Check if the model is fully outside the field.
        
        Returns:
            bool: True if the model is fully outside
        """
        if not self.m_model.is_out():
            loc = self.m_model.get_location()
            w = self.m_field.get_w()
            h = self.m_field.get_h()
            
            # Check all parts of the shape
            if self.m_shape:
                for rel_loc in self.m_shape.get_rel_locs():
                    position = loc.plus(rel_loc)
                    x, y = position.get_x(), position.get_y()
                    
                    # Check if part is inside field
                    if 0 <= x < w and 0 <= y < h:
                        return False
            else:
                # Simplified for when shape is not available
                x, y = loc.get_x(), loc.get_y()
                if 0 <= x < w and 0 <= y < h:
                    return False
        
        return True
    
    @staticmethod
    def unique(models):
        """
        Remove duplicates from a list of models.
        
        Args:
            models (list): The list to modify
        """
        seen = set()
        unique_models = []
        for model in models:
            if model not in seen:
                seen.add(model)
                unique_models.append(model)
        
        # Update original list in-place
        models.clear()
        models.extend(unique_models)