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

from gengine.drawable import Drawable

class MultiDrawer(Drawable):
    """
    Container for drawable objects.
    Manages a collection of drawable objects and draws them in order.
    """
    
    def __init__(self):
        """
        Initialize a new multi-drawer.
        """
        self.drawers = []
    
    def accept_drawer(self, drawer):
        """
        Add a drawer to the end of the list.
        
        Args:
            drawer (Drawable): The drawer to add
        """
        self.drawers.append(drawer)
    
    def remove_drawer(self, drawer):
        """
        Remove a drawer from the list.
        The drawer will not be deleted.
        
        Args:
            drawer (Drawable): The drawer to remove
        """
        if drawer in self.drawers:
            self.drawers.remove(drawer)
    
    def remove_all(self):
        """
        Remove all drawers from the list.
        """
        self.drawers.clear()
    
    def draw_on(self, screen):
        """
        Let every registered drawer draw on the screen.
        
        Args:
            screen (pygame.Surface): The surface to draw on
        """
        for drawer in self.drawers:
            drawer.draw_on(screen)