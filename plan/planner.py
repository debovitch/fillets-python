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
from plan.subtitle_agent import SubTitleAgent
from plan.fish_dialog import FishDialog
from plan.command_queue import CommandQueue
from plan.script_cmd import ScriptCmd

class Planner(NoCopy):
    """
    Planner for game actions and dialogs.
    Coordinates command execution and dialog display.
    """
    
    def __init__(self):
        """Initialize a new planner."""
        self.fish_dialog = FishDialog()
        self.plan = CommandQueue()
        self.subtitle_agent = SubTitleAgent.get_instance()
        self.fish_dialog.set_subtitle_agent(self.subtitle_agent)
    
    def __del__(self):
        """Clean up resources."""
        # Python will handle the garbage collection
        pass
    
    def dialogs(self):
        """
        Get the fish dialog handler.
        
        Returns:
            FishDialog: The fish dialog handler
        """
        return self.fish_dialog
    
    def planner_help(self, state):
        """
        Show help for the planner.
        
        Args:
            state: The game state
        """
        # This would typically show help text or a help screen
        # For now, we'll just pass
        pass
    
    def subtitle_toggle(self):
        """Toggle subtitles on/off."""
        from gengine.agent.option_agent import OptionAgent
        
        # Get current subtitle setting
        option = OptionAgent.agent()
        subtitles = option.get_as_bool("subtitles", True)
        
        # Toggle setting
        option.set_persistent("subtitles", "1" if not subtitles else "0")
    
    def get_subtitle_agent(self):
        """
        Get the subtitle agent.
        
        Returns:
            SubTitleAgent: The subtitle agent
        """
        return self.subtitle_agent
    
    def register_drawable(self, drawer):
        """
        Register the subtitle agent as a drawable.
        
        Args:
            drawer: The drawer to register with
        """
        drawer.accept_drawer(self.subtitle_agent)
        
    def kill_plan(self):
        """
        Kill the current plan.
        Cancel all pending dialogs and commands.
        """
        if hasattr(self, 'fish_dialog') and self.fish_dialog:
            self.fish_dialog.kill_talks()
        self.interrupt_plan()
            
    def satisfy_plan(self):
        """
        Check if the current plan is satisfied.
        
        Returns:
            bool: True if the plan is satisfied
        """
        self.fish_dialog.update_stack()
        self.plan.execute_first()
        return self.plan.empty()

    def update_plan(self):
        """Execute one planned action tick."""
        return self.satisfy_plan()

    def interrupt_plan(self):
        """Remove all queued planned actions."""
        self.plan.remove_all()

    def plan_action(self, script_state, func_ref):
        """Plan a Lua function to be called until it returns true."""
        if not isinstance(func_ref, int):
            func_ref = script_state.ref(func_ref)
        self.plan.plan_command(ScriptCmd(script_state, func_ref))

    def is_planning(self):
        """Return true when there is a planned command in the queue."""
        return not self.plan.empty()
