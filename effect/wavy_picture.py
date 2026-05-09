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

import math

import pygame

from effect.picture import Picture
from gengine.agent.timer_agent import TimerAgent


class WavyPicture(Picture):
    """
    Picture drawn with the same horizontal water-wave distortion used by
    the original Fillets NG background renderer.
    """

    def __init__(self, file_or_surface, loc):
        """
        Initialize the picture.

        Args:
            file_or_surface: Either a file path or a pygame.Surface
            loc: The location of the picture on screen
        """
        super().__init__(file_or_surface, loc)
        self.amplitude = 0.0
        self.periode = float(self.surface.get_width())
        self.speed = 0.0

    def set_wamp(self, amplitude):
        """
        Set wave amplitude.

        Args:
            amplitude (float): Horizontal wave amplitude in pixels
        """
        self.amplitude = float(amplitude)

    def set_wperiode(self, periode):
        """
        Set wave period.

        Args:
            periode (float): Vertical period divisor used in the sine phase
        """
        self.periode = float(periode)

    def set_wspeed(self, speed):
        """
        Set wave animation speed.

        Args:
            speed (float): Per-cycle phase increment
        """
        self.speed = float(speed)

    def draw_on(self, screen):
        """
        Draw the picture with a per-line horizontal sine shift.

        Args:
            screen (pygame.Surface): The surface to draw on
        """
        if self.amplitude == 0 or self.periode == 0:
            super().draw_on(screen)
            return

        width = self.surface.get_width()
        height = self.surface.get_height()
        loc_x = int(self.loc.get_x())
        loc_y = int(self.loc.get_y())
        phase_shift = TimerAgent.agent().get_cycles() * self.speed

        for py in range(height):
            shift_x = int(0.5 + self.amplitude * math.sin(py / self.periode + phase_shift))
            self._draw_shifted_row(screen, py, shift_x, width, loc_x, loc_y)

    def _draw_shifted_row(self, screen, py, shift_x, width, loc_x, loc_y):
        """
        Draw one source row using the same clipping/padding behavior as the
        SDL implementation.
        """
        if shift_x == 0:
            screen.blit(self.surface, (loc_x, loc_y + py), pygame.Rect(0, py, width, 1))
            return

        if shift_x > 0:
            shift_x = min(shift_x, width)
            main_width = width - shift_x
            if main_width > 0:
                screen.blit(
                    self.surface,
                    (loc_x, loc_y + py),
                    pygame.Rect(shift_x, py, main_width, 1),
                )

            pad_x = width - shift_x
            if shift_x > 0:
                screen.blit(
                    self.surface,
                    (loc_x + pad_x, loc_y + py),
                    pygame.Rect(pad_x, py, shift_x, 1),
                )
            return

        shift_x = max(shift_x, -width)
        pad_width = -shift_x
        main_width = width - pad_width

        if pad_width > 0:
            screen.blit(
                self.surface,
                (loc_x, loc_y + py),
                pygame.Rect(0, py, pad_width, 1),
            )
        if main_width > 0:
            screen.blit(
                self.surface,
                (loc_x + pad_width, loc_y + py),
                pygame.Rect(0, py, main_width, 1),
            )
