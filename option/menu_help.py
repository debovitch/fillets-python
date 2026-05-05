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
Help overlay.
"""

import pygame

from effect.font import Font
from effect.surface_tool import SurfaceTool
from gengine.agent.option_agent import OptionAgent
from gengine.path import Path
from gengine.v2 import V2
from option.help_input import HelpInput
from plan.game_state import GameState
from widget.labels import Labels
from widget.wi_para import WiPara


class MenuHelp(GameState):
    """
    Help screen shown over the current state.
    """

    def __init__(self):
        """Initialize the help overlay."""
        GameState.__init__(self)

        used_font = Font(Path.data_read_path("font/font_menu.ttf"), 14)
        used_color = (255, 255, 255, 255)
        labels = Labels(Path.data_read_path("script/labels.lua"))
        self.help = WiPara(labels.get_label("help"), used_font, used_color)
        labels.labels.remove_all()

        self.take_handler(HelpInput(self))

    def get_name(self):
        """
        Get state name.

        Returns:
            str: State name
        """
        return "state_help"

    def allow_bg(self):
        """
        Allow lower states to keep running in the background.

        Returns:
            bool: Always True
        """
        return True

    def own_init_state(self):
        """Initialize the help overlay."""
        self.own_resume_state()

    def own_update_state(self):
        """Update help overlay."""
        pass

    def own_pause_state(self):
        """Pause help overlay."""
        pass

    def own_resume_state(self):
        """Center help text on the current screen."""
        options = OptionAgent.agent()
        screen_w = options.get_as_int("screen_width")
        screen_h = options.get_as_int("screen_height")
        self.help.set_shift(V2(
            (screen_w - self.help.get_w()) // 2,
            (screen_h - self.help.get_h()) // 2
        ))

    def own_clean_state(self):
        """Clean help overlay."""
        self.help = None

    def draw_on(self, screen):
        """
        Draw the help overlay.

        Args:
            screen: Pygame screen surface
        """
        SurfaceTool.alpha_fill(screen, None, pygame.Color(0, 0, 0, 129))
        if self.help:
            self.help.draw_on(screen)
