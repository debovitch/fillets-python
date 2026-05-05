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
from gengine.exceptions import LogicException
from gengine.ex_info import ExInfo

class LevelCountDown(NoCopy):
    """
    Countdowns finished or wrong state.
    """
    
    def __init__(self, access):
        """
        Prepare countdown.
        
        Args:
            access: RoomAccess object that provides access to the Room
        """
        self.countdown = -1
        self.access = access
        self.level_status = None
    
    def fill_status(self, status):
        """Set the level status object."""
        self.level_status = status
    
    def reset(self):
        """
        Resets counter.
        
        Raises:
            LogicException: when level_status is not filled
        """
        if self.level_status is None:
            raise LogicException(ExInfo("level status is None"))
        
        self.level_status.set_running(True)
        self.countdown = -1
    
    def count_down(self, advisor):
        """
        Countdown to zero.
        
        Args:
            advisor: Advisor which knows usable countdown values
            
        Returns:
            bool: True when counter is at zero
        """
        result = False
        
        if self.countdown < 0:
            self._set_count_down(advisor)
        elif self.countdown > 0:
            self.countdown -= 1
        else:
            result = True
            
        return result
    
    def _set_count_down(self, advisor):
        """
        Set countdown value based on room state.
        
        Args:
            advisor: CountAdvisor providing countdown values
        """
        room = self.access.const_room()
        
        if room.is_solved():
            self.countdown = advisor.get_count_for_solved()
        elif room.cannot_move():
            self.countdown = advisor.get_count_for_wrong()
        else:
            self.countdown = -1
    
    def is_finished_enough(self):
        """Check if solved and countdown reached zero."""
        return self.countdown == 0 and self.access.const_room().is_solved()
    
    def is_wrong_enough(self):
        """Check if stuck and countdown reached zero."""
        room = self.access.const_room()
        return (self.countdown == 0 and 
                room.cannot_move() and 
                not room.is_solved())
    
    def save_solution(self):
        """
        Write best solution to file.
        Save moves and models state.
        """
        self.level_status.set_complete()
        current_moves = self.access.const_room().step_counter().get_moves()
        self.level_status.write_solved_moves(current_moves)
    
    def create_next_state(self):
        """
        Creates next state or returns None.
        
        Returns:
            GameState or None: returns None when only quit_state() is needed
        """
        return self.level_status.create_poster()