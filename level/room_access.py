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

from gengine.no_copy import NoCopy
from gengine.ex_info import ExInfo
from gengine.exceptions import LogicException

class RoomAccess(NoCopy):
    """
    Interface to access a changing room.
    Provides a way to manage access to the current room.
    """
    
    def __init__(self):
        """Initialize a new room access."""
        self._room = None
    
    def __del__(self):
        """Clean up when the room access is deleted."""
        self.clean_room()
    
    def take_room(self, new_room):
        """
        Take ownership of a room.
        
        Args:
            new_room: The room to take ownership of
        """
        self.clean_room()
        self._room = new_room
    
    def clean_room(self):
        """Clean up the current room."""
        if self._room and hasattr(self._room, "clean"):
            self._room.clean()
        self._room = None
    
    def is_room(self):
        """
        Check if there is a room.
        
        Returns:
            bool: True if there is a room
        """
        return self._room is not None
    
    def check_room(self):
        """
        Check if there is a room.
        
        Raises:
            LogicException: If there is no room
        """
        if not self.is_room():
            raise LogicException(ExInfo("room is NULL"))
    
    def room(self):
        """
        Get the current room.
        
        Returns:
            Room: The current room
            
        Raises:
            LogicException: If there is no room
        """
        self.check_room()
        return self._room
    
    def const_room(self):
        """
        Get the current room (const version).
        
        Returns:
            Room: The current room
            
        Raises:
            LogicException: If there is no room
        """
        self.check_room()
        return self._room
