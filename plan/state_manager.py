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
State manager for game states.
"""

from gengine.no_copy import NoCopy
from gengine.log import log_debug

class StateManager(NoCopy):
    """
    Manages game states and transitions.
    Maintains a stack of game states.
    """
    
    def __init__(self):
        """Initialize a new state manager."""
        NoCopy.__init__(self)
        self.states = []
        self.next_state = None
        self.next_state_parent = None
        self.remove_state = False
        self.remove_state_target = None
        self.change_state_target = None
        self.installed_drawers = []
    
    def update_game(self):
        """
        Update the current game state.
        Handle state transitions.
        """
        # Handle state transitions
        self.handle_next_state()
        
        # Update running states from bottom to top.
        for state in list(self.states):
            if state.is_running():
                state.update_state()
    
    def handle_next_state(self):
        """Handle state transitions."""
        if self.change_state_target is not None:
            self.do_change_state(self.change_state_target, self.next_state)
            self.change_state_target = None
            self.next_state = None
            self.next_state_parent = None
            return

        if self.remove_state:
            self.do_pop_state(self.remove_state_target)
            self.remove_state = False
            self.remove_state_target = None
        
        if self.next_state:
            self.do_push_state(self.next_state, self.next_state_parent)
            self.next_state = None
            self.next_state_parent = None
    
    def push_state(self, prev_state=None, new_state=None):
        """
        Push a new state onto the stack.
        
        Args:
            prev_state: The previous state (for bg detection, can be None)
            new_state: The new state to push
        """
        if new_state is None:
            new_state = prev_state
            prev_state = self.states[-1] if self.states else None

        self.next_state = new_state
        self.next_state_parent = prev_state
    
    def change_state(self, new_state):
        """
        Change to a new state.
        Pop the current state and push the new one.
        
        Args:
            new_state: The new state
        """
        self.change_state_target = self.states[-1] if self.states else None
        self.next_state = new_state
        self.next_state_parent = None
    
    def pop_state(self):
        """Pop the current state from the stack."""
        self.remove_state = True
        self.remove_state_target = self.states[-1] if self.states else None
    
    def do_push_state(self, new_state, prev_state=None):
        """
        Actually push a new state onto the stack.
        
        Args:
            new_state: The new state to push
        """
        # Push and initialize new state
        if prev_state and prev_state in self.states:
            index = self.states.index(prev_state) + 1
            self.states.insert(index, new_state)
        else:
            self.states.append(new_state)
        new_state.init_state(self)
        self.check_stack()

    def do_change_state(self, target, new_state):
        """
        Replace one state without resuming the state below it first.

        This matches the original C++ StateManager::changeState behavior.
        """
        current = target if target in self.states else (self.states[-1] if self.states else None)
        if current is None:
            self.states.append(new_state)
            new_state.init_state(self)
            self.install_handlers()
            return

        index = self.states.index(current)
        current.clean_state()
        self.states[index] = new_state
        new_state.init_state(self)
        self.check_stack()
    
    def do_pop_state(self, target=None):
        """Actually pop the current state from the stack."""
        if not self.states:
            return
        
        # Clean up current state
        current = target if target in self.states else self.states[-1]
        self.states.remove(current)
        current.clean_state()
        
        if self.states:
            self.check_stack()
        else:
            self.uninstall_handlers()
            from gengine.agent.messager_agent import MessagerAgent
            from gengine.message.simple_msg import SimpleMsg
            from gengine.name import Name
            MessagerAgent.agent().forward_new_msg(SimpleMsg(Name.APP_NAME, "quit"))

    def check_stack(self):
        """Keep the active/background state stack consistent."""
        if not self.states:
            self.uninstall_handlers()
            return

        should_run = True
        for index in range(len(self.states) - 1, -1, -1):
            state = self.states[index]

            if should_run:
                if index == len(self.states) - 1:
                    if state.is_on_bg():
                        state.note_fg()
                else:
                    state.note_bg()

                if not state.is_running():
                    state.resume_state()
            elif state.is_running():
                state.pause_state()

            should_run = should_run and state.allow_bg()

        self.install_handlers()

    def install_handlers(self):
        """Install input and drawing for the current top state."""
        from gengine.agent.input_agent import InputAgent
        from gengine.agent.video_agent import VideoAgent

        self.uninstall_handlers()
        if not self.states:
            return

        current = self.states[-1]
        InputAgent.agent().install_handler(getattr(current, "handler", None))

        for state in self.states:
            if state.is_running() and hasattr(state, "draw_on"):
                VideoAgent.agent().accept_drawer(state)
                self.installed_drawers.append(state)

    def uninstall_handlers(self):
        """Remove handlers installed by the state manager."""
        from gengine.agent.input_agent import InputAgent
        from gengine.agent.video_agent import VideoAgent

        InputAgent.agent().install_handler(None)
        for drawer in self.installed_drawers:
            VideoAgent.agent().remove_drawer(drawer)
        self.installed_drawers = []
    
    def get_state_count(self):
        """
        Get the number of states on the stack.
        
        Returns:
            int: Number of states
        """
        return len(self.states)
