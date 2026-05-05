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

class LoadException(Exception):
    """Exception raised when loading fails."""
    def __init__(self, info):
        self.info = info
        super().__init__(str(info))

class LevelLoading(NoCopy):
    """
    Game loading.
    Handles loading saved games and replays.
    """
    
    SPEED_REPLAY = 1
    
    def __init__(self, access):
        """
        Initialize level loading.
        
        Args:
            access: RoomAccess instance
        """
        self._access = access
        self.reset()
    
    def reset(self):
        """Reset loading state."""
        self._paused = False
        self._replay_mode = False
        self._load_speed = 1
        self._loaded_moves = ""
    
    def set_load_speed(self, load_speed):
        """
        Set the speed for loading moves.
        
        Args:
            load_speed: Speed multiplier for loading
        """
        self._load_speed = load_speed
    
    def load_game(self, moves):
        """
        Start loading mode.
        
        Args:
            moves: Saved moves to load
        """
        self._loaded_moves = moves
        self._load_speed = min(50, max(5, len(self._loaded_moves) // 150))
    
    def load_replay(self, moves):
        """
        Start replay mode.
        
        Args:
            moves: Saved moves to load
        """
        self._loaded_moves = moves
        self._load_speed = 1
        self._replay_mode = True
    
    def toggle_pause(self):
        """Toggle pause state."""
        self._paused = not self._paused
    
    def is_paused(self):
        """
        Check if loading is paused.
        
        Returns:
            bool: True if paused
        """
        return self._paused
    
    def is_loading(self):
        """
        Check if loading is in progress.
        
        Returns:
            bool: True if loading
        """
        return bool(self._loaded_moves) or self._replay_mode
    
    def next_load_action(self):
        """
        Load a few moves.
        
        Raises:
            LoadException: If loading fails
        """
        if self._paused:
            return
            
        if not self._loaded_moves:
            self._access.room().begin_fall(False)
            self._access.room().finish_round(False)
        else:
            for i in range(min(self._load_speed, len(self._loaded_moves))):
                try:
                    symbol = self._loaded_moves[0]
                    self._loaded_moves = self._loaded_moves[1:]
                    
                    self._access.room().load_move(symbol)
                except LoadException as e:
                    raise LoadException(ExInfo(e.info).add_info("remain", self._loaded_moves))