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
from gengine.agent.base_agent import BaseAgent
from gengine.agent.option_agent import OptionAgent
from gengine.drawable import Drawable
from gengine.name import Name
from gengine.path import Path
from plan.fish_dialog import DialogMode
from plan.title import Title


class _PygameFontAdapter:
    """Fallback with the same small API as effect.font.Font."""

    def __init__(self, size):
        self.font = pygame.font.SysFont("Arial", size)

    def calc_text_width(self, text):
        return self.font.size(text)[0]

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


class SubTitleAgent(BaseAgent, Drawable):
    """Agent that scrolls level subtitles."""

    _instance = None

    TITLE_ROW = 26
    TITLE_BASE = 20
    TITLE_SPEED = 2
    TITLE_BORDER = 20
    TITLE_LIMIT_Y = TITLE_BASE + 5 * TITLE_ROW
    FONT_SIZE = 20
    DEFAULT_COLOR = (255, 255, 255, 255)

    @staticmethod
    def get_instance():
        try:
            from gengine.agent.agent_pack import AgentPack

            agent = AgentPack.get_agent(Name.SUBTITLE_NAME)
            if isinstance(agent, SubTitleAgent):
                return agent
        except Exception:
            pass

        if SubTitleAgent._instance is None:
            SubTitleAgent._instance = SubTitleAgent()
        return SubTitleAgent._instance

    def __init__(self):
        BaseAgent.__init__(self)
        SubTitleAgent._instance = self
        self.font = None
        self.fonts = {}
        self.titles = []
        self.limit_y = self.TITLE_LIMIT_Y
        self.mode = DialogMode.NORMAL
        self.end_msgs = []

    def get_name(self):
        return Name.SUBTITLE_NAME

    def own_init(self):
        self._ensure_font()

    def own_update(self):
        if not self.titles:
            return

        self.shift_titles_up(self.TITLE_SPEED)
        if self.titles and self.titles[0].is_gone():
            self.titles.pop(0)

        if not self.titles and self.end_msgs:
            for msg in self.end_msgs:
                msg.send()
            self.end_msgs = []

    def own_shutdown(self):
        self.remove_all()
        self.font = None

    def _ensure_font(self):
        if self.font:
            return

        try:
            font_path = Path.data_read_path("font/font_subtitle.ttf")
            self.font = Font(font_path, self.FONT_SIZE)
        except Exception:
            pygame.font.init()
            self.font = _PygameFontAdapter(self.FONT_SIZE)

    def _screen_width(self):
        try:
            return OptionAgent.agent().get_as_int("screen_width", 640)
        except Exception:
            return 640

    def _subtitles_enabled(self):
        try:
            return OptionAgent.agent().get_as_bool("subtitles", True)
        except Exception:
            return True

    def _color_tuple(self, color):
        if color is None:
            return self.DEFAULT_COLOR
        if hasattr(color, "to_tuple"):
            return color.to_tuple()
        if len(color) == 3:
            return color + (255,)
        return color

    def add_font(self, name, color):
        """Register a subtitle font color."""
        self.fonts[name] = self._color_tuple(color)

    def set_mode(self, mode):
        self.mode = mode

    def get_limit_y(self):
        return self.limit_y

    def set_limit_y(self, limit_y):
        self.limit_y = limit_y

    def plan_subtitle(self, dialog_pair, end_msg):
        """Compatibility entry point for code that plans a raw subtitle."""
        if not dialog_pair or dialog_pair.is_empty():
            return

        self.new_subtitle(dialog_pair.get_subtitle(), "")
        if end_msg:
            self.end_msgs.append(end_msg)

    def new_subtitle(self, original, fontname=""):
        """Create a new scrolling subtitle."""
        self._ensure_font()
        color = self.fonts.get(fontname, self.DEFAULT_COLOR)

        subtitle = (original or "").strip()
        while subtitle:
            subtitle = self.split_and_create(subtitle, color)

    def split_and_create(self, original, color):
        subtitle = original
        max_width = max(1, self._screen_width() - 2 * self.TITLE_BORDER)

        while subtitle and self.font.calc_text_width(subtitle) > max_width:
            subtitle = self.trim_rest(subtitle)

        if not subtitle:
            return ""

        self.new_short_subtitle(subtitle, color)
        return original[len(subtitle):].lstrip()

    def trim_rest(self, buffer):
        for index in range(len(buffer) - 1, -1, -1):
            if buffer[index] == " " and not (
                index - 2 >= 0 and buffer[index - 2] == " "
            ):
                return buffer[:index]

        if len(buffer) > 4:
            return buffer[:-4]
        return ""

    def new_short_subtitle(self, subtitle, color):
        start_y = self.lowest_y()
        final_y = self.TITLE_BASE + self.TITLE_ROW
        bonus_time = (
            self.TITLE_BASE - start_y + self.limit_y - self.TITLE_LIMIT_Y
        ) // self.TITLE_SPEED
        title = Title(start_y, final_y, bonus_time, self.limit_y,
                      subtitle, self.font, color)

        self.shift_finals_up(self.TITLE_ROW)
        self.titles.append(title)

    def shift_titles_up(self, rate):
        for title in self.titles:
            title.shift_up(rate)

    def shift_finals_up(self, rate):
        for title in self.titles:
            title.shift_final_up(rate)

    def lowest_y(self):
        lowest = self.TITLE_BASE
        if self.titles:
            latest = self.titles[-1].get_y() - self.TITLE_ROW
            lowest = min(lowest, latest)
        return lowest

    def kill_talks(self):
        self.titles = []
        self.end_msgs = []

    def hide_subtitle(self):
        self.kill_talks()

    def remove_all(self):
        self.kill_talks()
        self.fonts.clear()

    def draw_on(self, screen):
        if not self._subtitles_enabled():
            return

        for title in self.titles:
            title.draw_on(screen)
