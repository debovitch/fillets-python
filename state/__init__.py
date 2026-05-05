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
State package for the Fish Fillets NG game.
Contains classes for managing game states like demos, posters, and movies.
"""

from state.demo_input import DemoInput
from state.demo_mode import DemoMode
from state.game_input import GameInput
from state.poster_state import PosterState
from state.poster_scroller import PosterScroller
from state.movie_state import MovieState

__all__ = [
    'DemoInput',
    'DemoMode',
    'GameInput',
    'PosterState',
    'PosterScroller',
    'MovieState'
]