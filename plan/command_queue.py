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
Queue for sequential commands.
"""

from gengine.no_copy import NoCopy
from collections import deque

class CommandQueue(NoCopy):
    """Queue for executing sequential commands."""
    
    def __init__(self):
        """Initialize a new command queue."""
        NoCopy.__init__(self)
        self.commands = deque()
        self.count = 0
    
    def plan_command(self, new_command):
        """
        Add a new command to the end of the queue.
        
        Args:
            new_command: The command to add
        """
        self.commands.append(new_command)
    
    def execute_first(self):
        """
        Execute the first command in the queue.
        
        If the command returns True (indicating it's finished), 
        remove it from the queue. If the queue is empty, does nothing.
        
        Returns:
            bool: True if a command was executed, False otherwise
        """
        if not self.commands:
            return False
        
        command = self.commands[0]
        if command.finish(self.count):
            self.commands.popleft()
            self.count = 0
        else:
            self.count += 1
            
        return True
    
    def remove_all(self):
        """Remove all commands from the queue."""
        self.commands.clear()
        self.count = 0
    
    def empty(self):
        """
        Check if the queue is empty.
        
        Returns:
            bool: True if the queue is empty, False otherwise
        """
        return len(self.commands) == 0