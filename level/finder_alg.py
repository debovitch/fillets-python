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
Algorithm for finding paths.
"""

from collections import deque

from level.dir import Dir
from level.finder_field import FinderField
from level.finder_place import FinderPlace
from gengine.v2 import V2


class FinderAlg:
    """Algorithm to find the first direction of the shortest path."""

    def __init__(self, width_or_field, height_or_dest=None):
        # C++ form used by Room: FinderAlg(width, height)
        if isinstance(width_or_field, int) and isinstance(height_or_dest, int):
            self.m_closed = FinderField(width_or_field, height_or_dest)
            self.m_unit = None
            self.m_fifo = deque()
            self._legacy_dest_model = None
            self._legacy_field = None
            return

        # Compatibility form used by older Python demo tests:
        # FinderAlg(field, dest_model)
        self._legacy_field = width_or_field
        self._legacy_dest_model = height_or_dest
        self.m_closed = FinderField(width_or_field)
        self.m_unit = None
        self.m_fifo = deque()
        self.m_begin = None
        self.m_found = None

    def find_dir(self, unit, dest):
        """
        Find the best start direction to the destination.

        Args:
            unit: Unit that finds a path.
            dest: Destination field position.

        Returns:
            Dir: First direction to take, or DIR_NO.
        """
        if self.m_unit:
            self.m_closed.reset()
            self.m_fifo.clear()
        self.m_unit = unit

        unit_loc = unit.get_loc()
        width = unit.get_w()
        height = unit.get_h()
        if self.is_in_rect(unit_loc, width, height, dest):
            return Dir.DIR_NO

        self.m_closed.mark_closed(unit_loc)
        self.m_fifo.append(FinderPlace(Dir.DIR_LEFT, unit_loc.plus(V2(-1, 0))))
        self.m_fifo.append(FinderPlace(Dir.DIR_RIGHT, unit_loc.plus(V2(1, 0))))
        self.m_fifo.append(FinderPlace(Dir.DIR_UP, unit_loc.plus(V2(0, -1))))
        self.m_fifo.append(FinderPlace(Dir.DIR_DOWN, unit_loc.plus(V2(0, 1))))

        while self.m_fifo:
            place = self.m_fifo.popleft()
            if self.try_place(place):
                if self.is_in_rect(place.get_loc(), width, height, dest):
                    return place.get_start_dir()

                self.push_next(place, V2(-1, 0))
                self.push_next(place, V2(1, 0))
                self.push_next(place, V2(0, -1))
                self.push_next(place, V2(0, 1))

        return Dir.DIR_NO

    def push_next(self, parent, shift):
        """Push an open neighbor into the FIFO."""
        loc = parent.get_loc().plus(shift)
        if not self.m_closed.is_closed(loc):
            self.m_closed.mark_closed(loc)
            self.m_fifo.append(FinderPlace(parent.get_start_dir(), loc))

    @staticmethod
    def is_in_rect(rect_loc, width, height, dest):
        rect_x = rect_loc.get_x()
        rect_y = rect_loc.get_y()
        dest_x = dest.get_x()
        dest_y = dest.get_y()
        return rect_x <= dest_x < rect_x + width and rect_y <= dest_y < rect_y + height

    def try_place(self, place):
        return self.m_unit.is_free_place(place.get_loc())

    # Compatibility method used by the older Python demo tests.
    def find_any_path(self, start_model):
        self.m_closed.reset()
        self.m_begin = FinderPlace(start_model.get_location(), None, self.m_closed)
        self.m_found = None
        queue = deque([self.m_begin])

        while queue and self.m_found is None:
            place = queue.popleft()
            model = self._legacy_field.get_model(place.get_location())
            if model == self._legacy_dest_model:
                self.m_found = place
                break

            for direction in (Dir.DIR_UP, Dir.DIR_RIGHT, Dir.DIR_DOWN, Dir.DIR_LEFT):
                shift = Dir.dir2xy(direction)
                next_loc = place.get_location().plus(shift)
                if self.m_closed.was_visited(next_loc):
                    continue
                model = self._legacy_field.get_model(next_loc)
                if model and model != self._legacy_dest_model:
                    continue
                queue.append(FinderPlace(next_loc, place, self.m_closed))

        return self.m_found is not None
