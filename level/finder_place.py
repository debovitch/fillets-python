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
Place used in pathfinding algorithm.
"""

from gengine.no_copy import NoCopy


class FinderPlace(NoCopy):
    """Place with the initial direction that reaches it."""

    def __init__(self, start_dir_or_loc, loc_or_prev=None, field=None):
        # C++ pathfinder form: FinderPlace(start_dir, loc)
        if field is None:
            self.m_start_dir = start_dir_or_loc
            self.m_loc = loc_or_prev
            self.m_prev = None
            return

        # Compatibility form used by the older Python demo tests:
        # FinderPlace(loc, prev, field)
        self.m_start_dir = None
        self.m_loc = start_dir_or_loc
        self.m_prev = loc_or_prev
        field.set_visited(self.m_loc)

    def get_loc(self):
        return self.m_loc

    def get_location(self):
        return self.m_loc

    def get_start_dir(self):
        return self.m_start_dir

    def get_prev(self):
        return self.m_prev

    def __str__(self):
        return f"Place({self.m_loc})"
