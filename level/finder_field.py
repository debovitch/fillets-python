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
Field used for path finding.
"""

from gengine.no_copy import NoCopy


class FinderField(NoCopy):
    """Closed-place map for path finding."""

    def __init__(self, width_or_field, height=None):
        if height is None:
            self.m_field = width_or_field
            self.m_w = self.m_field.get_w()
            self.m_h = self.m_field.get_h()
        else:
            self.m_field = None
            self.m_w = width_or_field
            self.m_h = height
        self.reset()

    def reset(self):
        """Erase all marks."""
        self.m_closed = [[False for _ in range(self.m_h)] for _ in range(self.m_w)]

    def mark_closed(self, loc):
        """Mark given place as closed."""
        x = loc.get_x()
        y = loc.get_y()
        if 0 <= x < self.m_w and 0 <= y < self.m_h:
            self.m_closed[x][y] = True

    def is_closed(self, loc):
        """Return true for closed places; outside the room is always closed."""
        x = loc.get_x()
        y = loc.get_y()
        if 0 <= x < self.m_w and 0 <= y < self.m_h:
            return self.m_closed[x][y]
        return True

    # Compatibility helpers used by the older Python demo tests.
    def get_model(self, loc):
        return self.m_field.get_model(loc) if self.m_field else None

    def was_visited(self, loc):
        return self.is_closed(loc)

    def set_visited(self, loc):
        self.mark_closed(loc)
