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

from enum import Enum

class Goal:
    """
    Goal conditions for game objects.
    Defines the conditions that must be satisfied for a level to be completed.
    """
    
    class Satisfy(Enum):
        """
        Enumeration of satisfaction states.
        """
        SATISFY_TRUE = 1
        SATISFY_FALSE = 2
        SATISFY_IGNORE = 3
    
    def __init__(self, out, alive):
        """
        Initialize a new goal.
        
        Args:
            out (Goal.Satisfy): Whether the object must be out of the room
            alive (Goal.Satisfy): Whether the object must be alive
        """
        self.out = out
        self.alive = alive
    
    @staticmethod
    def no_goal():
        """
        Create a goal that ignores all conditions.
        
        Returns:
            Goal: A goal with no conditions
        """
        return Goal(Goal.Satisfy.SATISFY_IGNORE, Goal.Satisfy.SATISFY_IGNORE)
    
    @staticmethod
    def out_goal():
        """
        Create a goal that requires the object to be out of the room.
        
        Returns:
            Goal: A goal requiring the object to be out
        """
        return Goal(Goal.Satisfy.SATISFY_TRUE, Goal.Satisfy.SATISFY_IGNORE)
    
    @staticmethod
    def escape_goal():
        """
        Create a goal that requires the object to escape alive.
        
        Returns:
            Goal: A goal requiring the object to be out and alive
        """
        return Goal(Goal.Satisfy.SATISFY_TRUE, Goal.Satisfy.SATISFY_TRUE)
    
    @staticmethod
    def alive_goal():
        """
        Create a goal that requires the object to be alive.
        
        Returns:
            Goal: A goal requiring the object to be alive
        """
        return Goal(Goal.Satisfy.SATISFY_IGNORE, Goal.Satisfy.SATISFY_TRUE)
    
    def is_satisfy(self, model):
        """
        Check if the model satisfies this goal.
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the model satisfies the goal
        """
        result = True
        
        if self.out == Goal.Satisfy.SATISFY_TRUE:
            result &= model.is_out()
        elif self.out == Goal.Satisfy.SATISFY_FALSE:
            result &= not model.is_out()
        
        if self.alive == Goal.Satisfy.SATISFY_TRUE:
            result &= model.is_alive()
        elif self.alive == Goal.Satisfy.SATISFY_FALSE:
            result &= not model.is_alive()
        
        return result
    
    def is_wrong(self, model):
        """
        Check if the goal cannot be satisfied anymore.
        Dead fish cannot be revived.
        Objects out of the room cannot go back.
        
        Args:
            model: The model to check
            
        Returns:
            bool: True if the goal cannot be satisfied
        """
        wrong = False
        
        if self.alive == Goal.Satisfy.SATISFY_TRUE:
            wrong |= not model.is_alive()
        
        if self.out == Goal.Satisfy.SATISFY_FALSE:
            wrong |= model.is_out()
            
        return wrong
    
    def should_go_out(self):
        """
        Check if this goal requires the object to be out of the room.
        
        Returns:
            bool: True if the object should go out
        """
        return self.out == Goal.Satisfy.SATISFY_TRUE