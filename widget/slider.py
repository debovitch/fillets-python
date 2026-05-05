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
from gengine.agent.option_agent import OptionAgent
from gengine.mouse_stroke import MouseStroke
from widget.i_widget import IWidget

class Slider(IWidget):
    """
    Slider for numeric options.
    """
    
    # Constants
    PIXELS_PER_VALUE = 2
    HEIGHT = 30
    
    def __init__(self, param, min_value=0, max_value=100):
        """
        Create slider for a parameter.
        
        Args:
            param (str): Parameter name
            min_value (int): Minimum value
            max_value (int): Maximum value
        """
        super().__init__()
        self.param = param
        self.min = min_value
        self.max = max_value
    
    def get_w(self):
        """
        Get slider width.
        
        Returns:
            int: Slider width
        """
        return (self.max - self.min) * self.PIXELS_PER_VALUE
    
    def get_h(self):
        """
        Get slider height.
        
        Returns:
            int: Slider height
        """
        return self.HEIGHT
    
    def value_to_slide(self, value):
        """
        Convert value to slider position.
        
        Args:
            value (int): Parameter value
            
        Returns:
            int: Position on slider
        """
        slide = value - self.min
        slide = max(slide, 0)
        slide = min(slide, self.max - self.min)
        return slide * self.PIXELS_PER_VALUE
    
    def slide_to_value(self, slide):
        """
        Convert slider position to value.
        
        Args:
            slide (int): Position on slider
            
        Returns:
            int: Parameter value
        """
        value = slide / self.PIXELS_PER_VALUE + self.min
        return int(value + 0.5)  # Round to nearest integer
    
    def own_mouse_button(self, stroke):
        """
        Handle mouse button.
        
        Args:
            stroke (MouseStroke): Mouse button event
        """
        if stroke.is_left():
            inside = stroke.get_loc().minus(self.shift)
            value = self.slide_to_value(inside.get_x())
            OptionAgent.agent().set_persistent(self.param, value)
    
    def draw_on(self, screen):
        """
        Draw the slider.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        value = OptionAgent.agent().get_as_int(self.param)
        
        # Draw background
        bg_rect = pygame.Rect(
            self.shift.get_x(),
            self.shift.get_y(),
            self.get_w(),
            self.get_h()
        )
        pygame.draw.rect(screen, (100, 100, 100), bg_rect)
        
        # Draw filled portion
        fill_rect = pygame.Rect(
            self.shift.get_x(),
            self.shift.get_y(),
            self.value_to_slide(value),
            self.get_h()
        )
        pygame.draw.rect(screen, (0, 255, 0), fill_rect)