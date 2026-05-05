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
Widget package for the Fish Fillets NG game.
Contains UI components for menus and options.
"""

from widget.i_widget import IWidget
from widget.wi_container import WiContainer
from widget.wi_box import WiBox
from widget.h_box import HBox
from widget.v_box import VBox
from widget.wi_picture import WiPicture
from widget.wi_space import WiSpace
from widget.slider import Slider
from widget.radio_box import RadioBox
from widget.wi_button import WiButton
from widget.wi_status_bar import WiStatusBar
from widget.wi_label import WiLabel
from widget.wi_para import WiPara
from widget.labels import Labels