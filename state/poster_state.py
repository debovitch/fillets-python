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
Static picture display state.
"""

from gengine.path import Path
from plan.game_state import GameState
from effect.picture import Picture
from gengine.v2 import V2
from state.demo_input import DemoInput
from gengine.agent.option_agent import OptionAgent
from gengine.agent.video_agent import VideoAgent

class PosterState(GameState):
    """Static picture display state."""
    
    def __init__(self, picture):
        """
        Initialize the poster state.
        
        Args:
            picture (Path): Path to the image file
        """
        GameState.__init__(self)
        self.bg = Picture(picture, V2(0, 0))
        self.take_handler(DemoInput(self))
        self.register_drawable(self.bg)
    
    def __del__(self):
        """Clean up resources when deleted."""
        self.bg = None
    
    def get_name(self):
        """
        Get the state name.
        
        Returns:
            str: The state name
        """
        return "state_poster"
    
    def own_init_state(self):
        """Initialize the poster state."""
        options = OptionAgent.get_instance()
        options.set_param("screen_width", self.bg.get_w())
        options.set_param("screen_height", self.bg.get_h())
        VideoAgent.get_instance().init_video_mode()
    
    def own_update_state(self):
        """Update the poster state (no-op)."""
        pass

    def draw_on(self, screen):
        """Draw the poster picture."""
        self.bg.draw_on(screen)
    
    def own_pause_state(self):
        """Pause the state (no-op)."""
        pass
    
    def own_resume_state(self):
        """Resume the state (no-op)."""
        pass
    
    def own_clean_state(self):
        """Clean up resources (no-op)."""
        pass
