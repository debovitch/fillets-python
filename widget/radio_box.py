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
from widget.wi_container import WiContainer

class RadioBox(WiContainer):
    """
    Radio box with picture background.
    """
    
    # Border size
    BORDER = 4
    
    def __init__(self, param, value, picture):
        """
        Initialize radio box.
        
        Args:
            param (str): Parameter name
            value (str): Parameter value
            picture (Path): Picture path
        """
        from widget.wi_picture import WiPicture
        super().__init__(WiPicture(picture), self.BORDER)
        self.param = param
        self.value = value
    
    def own_mouse_button(self, stroke):
        """
        Handle mouse button.
        
        Args:
            stroke (MouseStroke): Mouse button event
        """
        if stroke.is_left():
            OptionAgent.agent().set_persistent(self.param, self.value)
    
    def draw_on(self, screen):
        """
        Draw radio box with highlight if selected.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        current = OptionAgent.agent().get_param(self.param)
        
        if str(current) == str(self.value):
            # Draw green border for selected option
            rect = pygame.Rect(
                self.shift.get_x(),
                self.shift.get_y(),
                self.get_w(),
                self.get_h()
            )
            pygame.draw.rect(screen, (0, 255, 0), rect, width=self.BORDER)
        
        # Draw content
        super().draw_on(screen)