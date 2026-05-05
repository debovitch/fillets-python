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
from gengine.no_copy import NoCopy

class GameState(NoCopy):
    """
    Base class for all game states.
    Manages state transitions, initialization, updating, and cleanup.
    """
    
    def __init__(self):
        """Initialize a new game state."""
        self.active = False
        self.on_bg = False
        self.next_state = None
        self.handler = None
        self.drawer = None
        self.manager = None
    
    @abstractmethod
    def get_name(self):
        """
        Get the name of this state.
        
        Returns:
            str: The state name
        """
        pass
    
    def allow_bg(self):
        """
        Check if this state allows background states.
        
        Returns:
            bool: True if this state allows background states
        """
        return False
    
    def is_running(self):
        """
        Check if this state is running.
        
        Returns:
            bool: True if this state is running
        """
        return self.active
    
    def is_on_bg(self):
        """
        Check if this state is on background.
        
        Returns:
            bool: True if this state is on background
        """
        return self.on_bg
    
    def set_next_state(self, next_state):
        """
        Set the next state.
        
        Args:
            next_state: The next state
        """
        self.next_state = next_state
    
    def init_state(self, manager):
        """
        Initialize this state.
        
        Args:
            manager: The state manager
        """
        self.manager = manager
        self.active = True
        self.own_init_state()
    
    @abstractmethod
    def own_init_state(self):
        """Initialize this state (to be implemented by subclasses)."""
        pass
    
    def update_state(self):
        """Update this state."""
        if self.active:
            self.own_update_state()
    
    @abstractmethod
    def own_update_state(self):
        """Update this state (to be implemented by subclasses)."""
        pass
    
    def pause_state(self):
        """Pause this state."""
        if self.active:
            self.own_pause_state()
            self.active = False
            self.on_bg = False
    
    @abstractmethod
    def own_pause_state(self):
        """Pause this state (to be implemented by subclasses)."""
        pass
    
    def resume_state(self):
        """Resume this state."""
        if not self.active:
            self.active = True
            self.own_resume_state()
    
    @abstractmethod
    def own_resume_state(self):
        """Resume this state (to be implemented by subclasses)."""
        pass
    
    def clean_state(self):
        """Clean this state."""
        if self.active:
            self.own_clean_state()
            self.active = False
    
    @abstractmethod
    def own_clean_state(self):
        """Clean this state (to be implemented by subclasses)."""
        pass
    
    def note_bg(self):
        """Note that this state is now on background."""
        self.on_bg = True
        self.own_note_bg()
    
    def own_note_bg(self):
        """Note that this state is now on background (to be implemented by subclasses)."""
        pass
    
    def note_fg(self):
        """Note that this state is now on foreground."""
        self.on_bg = False
        self.own_note_fg()
    
    def own_note_fg(self):
        """Note that this state is now on foreground (to be implemented by subclasses)."""
        pass
    
    def quit_state(self):
        """Quit this state."""
        if self.next_state:
            next_state = self.next_state
            self.next_state = None
            self.change_state(next_state)
        elif self.manager:
            self.manager.pop_state()
    
    def push_state(self, new_state):
        """
        Push a new state onto the stack.
        
        Args:
            new_state: The new state
        """
        if self.manager:
            self.manager.push_state(self, new_state)
    
    def change_state(self, new_state):
        """
        Change to a new state.
        
        Args:
            new_state: The new state
        """
        if self.manager:
            self.manager.change_state(new_state)
    
    def register_drawable(self, drawable):
        """
        Register a drawable with this state.
        
        Args:
            drawable: The drawable to register
        """
        if self.drawer:
            self.drawer.accept_drawer(drawable)
    
    def deregister_drawable(self, drawable):
        """
        Deregister a drawable from this state.
        
        Args:
            drawable: The drawable to deregister
        """
        if self.drawer:
            self.drawer.remove_drawer(drawable)
    
    def take_handler(self, new_handler):
        """
        Take a new input handler.
        
        Args:
            new_handler: The new input handler
        """
        self.handler = new_handler
    
    def get_input(self):
        """
        Get the input provider.
        
        Returns:
            The input provider
        """
        if self.handler:
            return self.handler.get_provider()
        return None
