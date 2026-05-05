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

class Field(NoCopy):
    """
    Two dimensional game field.
    Stores game objects in a grid.
    """
    
    def __init__(self, width, height):
        """
        Initialize a new field with the given dimensions.
        
        Args:
            width (int): The width of the field
            height (int): The height of the field
        """
        self.width = width
        self.height = height
        
        # Create a 2D array of None
        self.marks = [[None for _ in range(height)] for _ in range(width)]
        
        # Border object (used for anything outside the field)
        from level.model_factory import ModelFactory
        self.border = ModelFactory.create_border()
        self.border.get_rules().take_field(self)
    
    def get_w(self):
        """
        Get the width of the field.
        
        Returns:
            int: The width of the field
        """
        return self.width
    
    def get_h(self):
        """
        Get the height of the field.
        
        Returns:
            int: The height of the field
        """
        return self.height
    
    def get_model(self, loc):
        """
        Get the model at the given location.
        
        Args:
            loc: V2 coordinates
            
        Returns:
            The model at the location, or the border if the location is outside the field
        """
        x, y = loc.get_x(), loc.get_y()

        if self.marks is None:
            return
        
        # Check if location is within field boundaries
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.marks[x][y]
        else:
            return self.border
    
    def set_model(self, loc, model, to_override):
        """
        Set the model at the given location.
        
        Args:
            loc: V2 coordinates
            model: The model to set
            to_override: The model expected to be already at this location
        """
        x, y = loc.get_x(), loc.get_y()
        
        # Check if location is within field boundaries
        if 0 <= x < self.width and 0 <= y < self.height:
            # Only override if the current model matches the expected one
            if to_override is None or self.marks[x][y] == to_override:
                self.marks[x][y] = model
    
    def __del__(self):
        """
        Clean up resources when the field is deleted.
        """
        # The border model and other models will be freed by Python's garbage collector
        self.border = None
