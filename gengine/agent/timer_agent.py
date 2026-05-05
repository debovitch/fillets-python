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

import pygame
from gengine.agent.base_agent import BaseAgent, agent_class
from gengine.name import Name
from gengine.agent.option_agent import OptionAgent

@agent_class(Name.TIMER_NAME)
class TimerAgent(BaseAgent):
    """
    Agent that handles timing and frame rate.
    Controls the game speed and provides delta time information.
    """
    
    def __init__(self):
        """
        Initialize the timer agent.
        """
        super().__init__()
        self.time_interval = 0
        self.last_time = 0
        self.next_time = 0
        self.delta_time = 1
        self.count = 0
    
    def own_init(self):
        """
        Initialize timing values.
        """
        self.time_interval = OptionAgent.agent().get_as_int("timeinterval", 100)
        self.last_time = pygame.time.get_ticks()
        self.next_time = self.last_time
        self.delta_time = 1
        self.count = 0
    
    def get_time_interval(self):
        """
        Get the time interval for the next frame.
        Game is faster with pressed Shift.
        
        Returns:
            int: The time interval in milliseconds
        """
        result = self.time_interval
        
        # Check if Shift is pressed
        mod_state = pygame.key.get_mods()
        if mod_state & pygame.KMOD_SHIFT:
            result = self.time_interval // 4
            
        return result
    
    def own_update(self):
        """
        Sleep for a fixed number of milliseconds to maintain a steady frame rate.
        """
        self.count += 1
        
        # Get current time
        now = pygame.time.get_ticks()
        
        # Sleep if we're ahead of schedule
        if now < self.next_time:
            pygame.time.delay(self.next_time - now)
        
        # Update timing values
        now = pygame.time.get_ticks()
        # NOTE: every cycle has a fixed time interval
        self.next_time = now + self.get_time_interval()
        
        self.delta_time = now - self.last_time
        self.last_time = now
    
    def get_delta_time(self):
        """
        Get the time elapsed since the last update.
        
        Returns:
            int: The delta time in milliseconds
        """
        return self.delta_time

    def get_time(self):
        """
        Get current pygame time in milliseconds.

        Returns:
            int: Milliseconds since pygame was initialized
        """
        return pygame.time.get_ticks()
    
    def get_cycles(self):
        """
        Get the number of update cycles that have been performed.
        
        Returns:
            int: The cycle count
        """
        return self.count
