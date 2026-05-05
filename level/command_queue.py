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

from collections import deque
from gengine.no_copy import NoCopy

class CommandQueue(NoCopy):
    """Queue of commands to be executed in order."""
    
    def __init__(self):
        """Initialize a new command queue."""
        self.commands = deque()
        self.count = 0
    
    def __del__(self):
        """Clean up when the command queue is deleted."""
        self.remove_all()
    
    def remove_all(self):
        """Remove all commands from the queue."""
        self.commands.clear()
        self.count = 0
    
    def plan_command(self, command):
        """
        Plan a command to be executed.
        
        Args:
            command: Command to plan
        """
        if command:
            self.commands.append(command)
    
    def execute_first(self):
        """
        Execute the first command in the queue.
        
        Returns:
            bool: True if a command was executed
        """
        if self.empty():
            return False

        command = self.commands[0]
        if command.finish(self.count):
            self.commands.popleft()
            self.count = 0
        else:
            self.count += 1

        return True
    
    def empty(self):
        """
        Check if the queue is empty.
        
        Returns:
            bool: True if the queue is empty
        """
        return len(self.commands) == 0
