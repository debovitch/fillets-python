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

from abc import ABC, abstractmethod

class StepCounter(ABC):
    """
    Interface to track the number of steps/moves in the game.
    This is an abstract base class that should be implemented by classes
    that need to track game moves.
    """
    
    @abstractmethod
    def get_step_count(self):
        """
        Get the total number of steps/moves taken.
        
        Returns:
            int: The number of steps
        """
        pass
    
    @abstractmethod
    def get_moves(self):
        """
        Get the sequence of moves taken.
        
        Returns:
            str: String representation of moves
        """
        pass
    
    @abstractmethod
    def is_powerful(self):
        """
        Check if the active unit has special/powerful capabilities.
        
        Returns:
            bool: True if the active unit is powerful
        """
        pass
    
    @abstractmethod
    def is_dangerous_move(self):
        """
        Check if the current move is dangerous.
        
        Returns:
            bool: True if the current move is dangerous
        """
        pass

# Concrete implementation for demo purposes
class SimpleStepCounter(StepCounter):
    """
    Simple implementation of StepCounter for demo purposes.
    """
    
    def __init__(self):
        """
        Initialize a new step counter.
        """
        self.steps = 0
        self.moves_list = ""
        self.units = []
    
    def get_step_count(self):
        """
        Get the total number of steps/moves taken.
        
        Returns:
            int: The number of steps
        """
        return self.steps
    
    def get_moves(self):
        """
        Get the sequence of moves taken.
        
        Returns:
            str: String representation of moves
        """
        return self.moves_list
    
    def is_powerful(self):
        """
        Check if the active unit has special/powerful capabilities.
        
        Returns:
            bool: True if the active unit is powerful
        """
        return False
    
    def is_dangerous_move(self):
        """
        Check if the current move is dangerous.
        
        Returns:
            bool: True if the current move is dangerous
        """
        return False
    
    def add_unit(self, unit):
        """
        Add a unit to be controlled.
        
        Args:
            unit: The unit to add
        """
        self.units.append(unit)
        
    def control_event(self, stroke):
        """
        Handle a control event.
        
        Args:
            stroke: The keystroke
        """
        # Just log the event for now
        self.steps += 1
        self.moves_list += "."
        
    def switch_active(self):
        """
        Switch the active unit.
        """
        # Not implemented for demo
        pass
        
    def make_move(self, move):
        """
        Make a move.
        
        Args:
            move (char): The move character
            
        Returns:
            bool: True for success
        """
        self.steps += 1
        self.moves_list += move
        return True
        
    def set_moves(self, moves):
        """
        Set the moves.
        
        Args:
            moves (str): The moves
        """
        self.moves_list = moves
        self.steps = len(moves)
        
    def cannot_move(self):
        """
        Check if no unit can move.
        
        Returns:
            bool: True if no unit can move
        """
        return len(self.units) == 0
        
    def check_active(self):
        """
        Check if active unit is valid.
        """
        # Not implemented for demo
        pass