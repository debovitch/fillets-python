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
Subtitle display.
"""

import pygame
from gengine.drawable import Drawable
from gengine.agent.option_agent import OptionAgent

class Title(Drawable):
    """Subtitle display at the bottom of the screen."""
    
    # Constants
    TIME_PER_CHAR = 2
    TIME_MIN = 40
    
    def __init__(self, base_y, final_y, bonus_time, limit_y, content, font, color):
        """
        Create a new title to draw.
        
        X is centered. Y is base_y above bottom screen border.
        
        Args:
            base_y (int): Number of pixels from the bottom border
            final_y (int): Final position, changes when next subtitle is added
            bonus_time (int): Bonus time for subtitle under bottom border
            limit_y (int): Max Y distance from bottom border
            content (str): Subtitle content
            font: Font to use for rendering
            color: Color to use for rendering
        """
        self.content = content
        self.font = font
        
        # Render the text surface
        self.surface = self.font.render_text_outlined(content, color)
        
        # Get screen dimensions from options
        self.screen_w = OptionAgent.get_instance().get_as_int("screen_width")
        self.screen_h = OptionAgent.get_instance().get_as_int("screen_height")
        
        # Calculate position
        text_width = self.font.calc_text_width(content)
        self.x = (self.screen_w - text_width) // 2
        self.y = self.screen_h - base_y
        self.final_y = self.screen_h - final_y
        self.limit_y = self.screen_h - limit_y
        
        # Calculate minimum display time based on text length
        import unicodedata
        self.mintime = len([c for c in content if not unicodedata.combining(c)]) * self.TIME_PER_CHAR
        if self.mintime < self.TIME_MIN:
            self.mintime = self.TIME_MIN
        self.mintime += bonus_time
    
    def draw_on(self, screen):
        """
        Draw the title on the screen.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        # Blit the rendered text at the current position
        screen.blit(self.surface, (self.x, self.y))
    
    def shift_up(self, rate):
        """
        Shift the title up until it reaches its final position.
        
        Args:
            rate (int): The rate at which to shift
        """
        self.mintime -= 1
        self.y -= rate
        if self.y < self.final_y:
            self.y = self.final_y
    
    def shift_final_up(self, rate):
        """
        Shift the final position up.
        
        Args:
            rate (int): The rate at which to shift
        """
        self.final_y -= rate
    
    def is_gone(self):
        """
        Check if the title has been displayed long enough.
        
        Returns:
            bool: True if the title should be removed
        """
        return self.mintime < 0 or self.y < self.limit_y
    
    def get_y(self):
        """
        Get the Y position from the bottom border.
        
        Returns:
            int: The distance from the bottom border
        """
        return self.screen_h - self.y
    
    def get_content(self):
        """
        Get the title's content.
        
        Returns:
            str: The title's content
        """
        return self.content