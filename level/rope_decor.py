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


class RopeDecor:
    """Draw a rope line between two models."""

    def __init__(self, model1, model2, shift1, shift2):
        self.model1 = model1
        self.model2 = model2
        self.shift1 = shift1
        self.shift2 = shift2

    def draw_on_screen(self, view, screen):
        loc1 = view.get_screen_pos(self.model1).plus(self.shift1)
        loc2 = view.get_screen_pos(self.model2).plus(self.shift2)
        pygame.draw.line(
            screen,
            (0x30, 0x40, 0x4e),
            (loc1.get_x(), loc1.get_y()),
            (loc2.get_x(), loc2.get_y()),
        )
