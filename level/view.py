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

import pygame
from gengine.drawable import Drawable
from gengine.v2 import V2
from level.dir import Dir

class View(Drawable):
    """
    View for model. Responsible for drawing models on screen.
    """
    # Scale factor for drawing
    SCALE = 15
    
    def __init__(self, models, w=0, h=0):
        """
        Create new view.
        
        Args:
            models: Field or ModelList containing models to draw
            w: Width of the view (for initialization)
            h: Height of the view (for initialization)
        """
        self.models = models
        self.width = w
        self.height = h
        self.decors = []
        self.anim_shift = 0
        self.shift_size = self.SCALE
        self.screen = None
        self.screen_shift = V2(0, 0)
    
    def __del__(self):
        """
        Clean up resources when the view is destroyed.
        """
        self.remove_decors()
    
    def remove_decors(self):
        """
        Remove all decorations.
        """
        self.decors.clear()
    
    def draw_decors(self):
        """
        Draw all decorations on the screen.
        """
        for decor in self.decors:
            if hasattr(decor, "draw_on_screen"):
                decor.draw_on_screen(self, self.screen)
            else:
                decor.draw_on(self.screen)
    
    def note_new_round(self, phases):
        """
        Prepare for a new animation round.
        
        Args:
            phases (int): Number of animation phases
        """
        self.anim_shift = 0
        self.compute_shift_size(phases)
    
    def compute_shift_size(self, phases):
        """
        Split move in a few phases.
        
        Args:
            phases (int): Number of phases for the animation
        """
        if phases > 0:
            self.shift_size = self.SCALE // phases
        else:
            self.shift_size = self.SCALE
    
    def draw_on(self, screen):
        """
        Draw models on the screen.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        self.screen = screen
        self.anim_shift = min(self.SCALE, self.anim_shift + self.shift_size)
        
        # Draw models
        if hasattr(self.models, 'draw_all_models'):
            # If it's a ModelList with a draw_all_models method
            self.models.draw_all_models(self)
        elif hasattr(self.models, 'foreach_model'):
            # If it's a Field with a foreach_model method
            def draw_func(model):
                self.draw_model(model)
            self.models.foreach_model(draw_func)
            
        self.draw_decors()
    
    def draw_model(self, model):
        """
        Draw a model on the screen.
        
        Args:
            model: The model to draw
        """
        if model and not model.is_lost():
            screen_pos = self.get_screen_pos(model)
            
            side = "left" if model.is_left() else "right"
            anim = getattr(model, 'anim', None)
            if anim:
                anim.draw_at(
                    self.screen, 
                    screen_pos.get_x(), 
                    screen_pos.get_y(), 
                    side
                )
    
    def get_screen_pos(self, model):
        """
        Returns position on screen where model will be drawn.
        
        Args:
            model: The model to position
            
        Returns:
            V2: The screen position
        """
        shift = V2(0, 0)
        dir = model.get_last_move_dir()
        
        if dir != Dir.DIR_NO:
            shift = Dir.dir2xy(dir)
            shift = shift.scale(self.anim_shift)
        
        shift = shift.plus(self.screen_shift)
        
        anim_shift = V2(0, 0)  # Default if model doesn't have anim
        anim = getattr(model, 'anim', None)
        if anim:
            anim_shift = anim.get_view_shift()
            
        return model.get_location().plus(anim_shift).scale(self.SCALE).plus(shift)
    
    def get_field_pos(self, cursor):
        """
        Returns position of tile under cursor.
        
        Args:
            cursor (V2): The cursor position
            
        Returns:
            V2: The field position
        """
        return cursor.minus(self.screen_shift).shrink(self.SCALE)
    
    def set_screen_shift(self, shift):
        """
        Set screen shift.
        
        Args:
            shift (V2): The screen shift
        """
        self.screen_shift = shift
    
    def add_decor(self, new_decor):
        """
        Add a decoration to the view.
        
        Args:
            new_decor: The decoration to add
        """
        self.decors.append(new_decor)
