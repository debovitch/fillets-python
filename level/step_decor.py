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

from effect.font import Font
from gengine.agent.option_agent import OptionAgent
from gengine.drawable import Drawable
from gengine.path import Path


class _PygameFontAdapter:
    """Fallback with the same small API as effect.font.Font."""

    def __init__(self, size):
        self.font = pygame.font.SysFont("Arial", size)

    def render_text(self, text, color):
        return self.font.render(text or " ", True, color)

    def render_text_outlined(self, text, color, outline_width=1):
        black = (0, 0, 0, 255)
        padded = " " + text + " "
        text_surface = self.render_text(padded, color)
        width, height = text_surface.get_size()
        surface = pygame.Surface(
            (width + outline_width * 2, height + outline_width * 2),
            pygame.SRCALPHA,
        )

        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx or dy:
                    surface.blit(
                        self.render_text(padded, black),
                        (outline_width + dx, outline_width + dy),
                    )
        surface.blit(text_surface, (outline_width, outline_width))
        return surface


class StepDecor(Drawable):
    """Draw number of steps in the top-right corner."""

    COLOR_ORANGE = (255, 197, 102, 255)
    COLOR_BLUE = (162, 244, 255, 255)

    def __init__(self, counter):
        self.counter = counter
        self.font = None
        self.current_text = None
        self.current_color = None
        self.text_surface = None

    def _ensure_font(self):
        if self.font:
            return

        try:
            self.font = Font(Path.data_read_path("font/font_console.ttf"), 20)
        except Exception:
            pygame.font.init()
            self.font = _PygameFontAdapter(20)

    def _show_steps(self):
        try:
            return OptionAgent.agent().get_as_bool("show_steps", True)
        except Exception:
            return True

    def draw_on(self, screen):
        if not self._show_steps():
            return

        self._ensure_font()
        color = self.COLOR_BLUE if self.counter.is_powerful() else self.COLOR_ORANGE
        text = str(self.counter.get_step_count())

        if (self.text_surface is None or self.current_text != text
                or self.current_color != color):
            self.current_text = text
            self.current_color = color
            self.text_surface = self.font.render_text_outlined(text, color)

        x = screen.get_width() - self.text_surface.get_width()
        screen.blit(self.text_surface, (x, 10))
