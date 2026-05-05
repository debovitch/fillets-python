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

from typing import Optional, Dict, List, Any, Tuple
import os

from gengine.no_copy import NoCopy
from gengine.v2 import V2
from gengine.script.scripter import Scripter
from gengine.path import Path
from gengine.ex_info import ExInfo
from gengine.log import log_info, log_warning, log_debug
from gengine.exceptions import LogicException
from gengine.multi_drawer import MultiDrawer
from gengine.agent.sound_agent import SoundAgent

# Forward declarations/imports
# These will need to be implemented as we progress
from level.phase_locker import PhaseLocker
from level.level_script import LevelScript
from level.level_loading import LevelLoading
from level.level_countdown import LevelCountDown
from level.command_queue import CommandQueue
from level.status_display import StatusDisplay
from level.level_input import LevelInput


class CountAdvisor:
    """Interface to advise countdown."""
    
    def get_count_for_solved(self) -> int:
        """Get the countdown for solved levels."""
        raise NotImplementedError("Subclasses must implement get_count_for_solved")
    
    def get_count_for_wrong(self) -> int:
        """Get the countdown for wrong levels."""
        raise NotImplementedError("Subclasses must implement get_count_for_wrong")


class GameState(NoCopy):
    """
    Game state base class.
    GameState manages input handlers and state transitions.
    """
    
    def __init__(self):
        """Initialize a new game state."""
        self.active = False
        self.on_bg = False
        self.next_state = None
        self.handler = None
        self.drawer = None
        self.manager = None
    
    def get_name(self) -> str:
        """Get the name of this game state."""
        raise NotImplementedError("Subclasses must implement get_name")
    
    def allow_bg(self) -> bool:
        """Check if this state allows background states."""
        return False
    
    def is_running(self) -> bool:
        """Check if this state is running."""
        return self.active
    
    def is_on_bg(self) -> bool:
        """Check if this state is on background."""
        return self.on_bg
    
    def set_next_state(self, next_state) -> None:
        """Set the next state."""
        self.next_state = next_state
    
    def own_init_state(self) -> None:
        """Initialize this state (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement own_init_state")
    
    def own_update_state(self) -> None:
        """Update this state (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement own_update_state")
    
    def own_pause_state(self) -> None:
        """Pause this state (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement own_pause_state")
    
    def own_resume_state(self) -> None:
        """Resume this state (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement own_resume_state")
    
    def own_clean_state(self) -> None:
        """Clean this state (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement own_clean_state")
    
    def own_note_bg(self) -> None:
        """Note that this state is now on background (to be implemented by subclasses)."""
        pass
    
    def own_note_fg(self) -> None:
        """Note that this state is now on foreground (to be implemented by subclasses)."""
        pass
    
    def init_state(self, manager) -> None:
        """Initialize this state with a manager."""
        self.manager = manager
        self.active = True
        self.own_init_state()
    
    def update_state(self) -> None:
        """Update this state."""
        if self.active:
            self.own_update_state()
    
    def pause_state(self) -> None:
        """Pause this state."""
        if self.active:
            self.own_pause_state()
            self.active = False
            self.on_bg = False
    
    def resume_state(self) -> None:
        """Resume this state."""
        if not self.active:
            self.active = True
            self.own_resume_state()
    
    def clean_state(self) -> None:
        """Clean this state."""
        if self.active:
            self.own_clean_state()
            self.active = False
    
    def quit_state(self) -> None:
        """Quit this state."""
        if self.next_state:
            next_state = self.next_state
            self.next_state = None
            self.change_state(next_state)
        elif self.manager:
            self.manager.pop_state()
    
    def push_state(self, new_state) -> None:
        """Push a new state onto the stack."""
        if self.manager:
            self.manager.push_state(self, new_state)
    
    def change_state(self, new_state) -> None:
        """Change to a new state."""
        if self.manager:
            self.manager.change_state(new_state)
    
    def note_bg(self) -> None:
        """Note that this state is now on background."""
        self.on_bg = True
        self.own_note_bg()
    
    def note_fg(self) -> None:
        """Note that this state is now on foreground."""
        self.on_bg = False
        self.own_note_fg()
    
    def register_drawable(self, drawable) -> None:
        """Register a drawable with this state."""
        if self.drawer:
            self.drawer.accept_drawer(drawable)
    
    def deregister_drawable(self, drawable) -> None:
        """Deregister a drawable from this state."""
        if self.drawer:
            self.drawer.remove_drawer(drawable)
    
    def take_handler(self, new_handler) -> None:
        """Take ownership of an input handler."""
        self.handler = new_handler
    
    def get_input(self):
        """Get the input provider."""
        if self.handler:
            return self.handler.get_provider()
        return None


class Level(GameState, CountAdvisor, Scripter):
    """
    Game level with room.
    This class manages the game level with its room, scripts, and game state.
    """
    
    # Class constants
    SPEED_REPLAY = 1
    
    def __init__(self, codename: str, datafile: Path, depth: int):
        """
        Create a new level.
        
        Args:
            codename: The codename of the level
            datafile: The path to the level data file
            depth: The depth of the level
        """
        GameState.__init__(self)
        Scripter.__init__(self)
        
        # Initialize member variables
        self.depth = depth
        self.desc = None
        self.codename = codename
        self.datafile = datafile
        self.new_round = False
        self.restart_counter = 1
        self.undo_steps = 0
        self.was_dangerous_move = False
        self.pending_replay_moves = None
        
        # Create components
        self.locker = PhaseLocker()
        self.level_script = LevelScript(self)
        self.loading = LevelLoading(self.level_script)
        self.countdown = LevelCountDown(self.level_script)
        self.show = CommandQueue()
        self.background = MultiDrawer()
        self.status_display = StatusDisplay()
        
        # Set up handlers and drawables
        self.take_handler(LevelInput(self))
        self.register_drawable(self.background)
        
        # Set up script functions
        self._register_script_functions()
    
    def get_name(self) -> str:
        """Get the name of this game state."""
        return "state_level"
    
    def fill_desc(self, desc) -> None:
        """Fill the level description."""
        self.desc = desc
    
    def fill_status(self, status) -> None:
        """Fill the level status."""
        self.countdown.fill_status(status)
    
    def _register_script_functions(self) -> None:
        """Register script functions for this level."""
        self.level_script.register_lua_functions(self.script)

        # Register functions to be called from Lua scripts
        self.script.register_function("room_create", self._script_create_room)
        self.script.register_function("room_createBg", self._script_create_background)
        self.script.register_function("room_addFish", self._script_add_fish)
        self.script.register_function("room_addModel", self._script_add_model)
        self.script.register_function("room_addDecor", self._script_add_decor)
        self.script.register_function("room_addGoal", self._script_add_goal)
        self.script.register_function("room_addRules", self._script_add_rules)
        self.script.register_function("game_save", self._script_save)
        self.script.register_function("game_load", self._script_load)
        self.script.register_function("game_saveUndo", self._script_save_undo)
        self.script.register_function("game_loadUndo", self._script_load_undo)
        self.script.register_function("game_loadFinalUndo", self._script_load_final_undo)
        self.script.register_function("game_saveState", self._script_save_state)
        self.script.register_function("game_loadState", self._script_load_state)
        
    def _script_create_room(self, script_state, w, h, picture):
        """
        Create a new room from Lua script.
        
        Args:
            script_state: Script state
            w (int): Room width
            h (int): Room height
            picture (str): Background picture path
            
        Returns:
            None
        """
        self.create_room(w, h, picture)
        return None
    
    def _script_create_background(self, script_state, picture):
        """
        Create a background from Lua script.
        
        Args:
            script_state: Script state
            picture (str): Background picture path
            
        Returns:
            None
        """
        if self.level_script.is_room():
            from gengine.path import Path
            img_path = Path.data_read_path(picture)
            self.level_script.room().create_background(img_path)
        return None
    
    def _script_add_fish(self, script_state, model_name, x, y, dir_name, shape_name):
        """
        Add a fish from Lua script.
        
        Args:
            script_state: Script state
            model_name (str): Model name
            x (int): X position
            y (int): Y position
            dir_name (str): Direction name
            shape_name (str): Shape name
            
        Returns:
            None
        """
        if self.level_script.is_room():
            self.level_script.room().add_fish(model_name, x, y, dir_name, shape_name)
        return None
    
    def _script_add_model(self, script_state, model_name, x, y, dir_name, shape_name):
        """
        Add a model from Lua script.
        
        Args:
            script_state: Script state
            model_name (str): Model name
            x (int): X position
            y (int): Y position
            dir_name (str): Direction name
            shape_name (str): Shape name
            
        Returns:
            None
        """
        if self.level_script.is_room():
            self.level_script.room().add_model(model_name, x, y, dir_name, shape_name)
        return None
    
    def _script_add_decor(self, script_state, decor_name, x, y):
        """
        Add decoration from Lua script.
        
        Args:
            script_state: Script state
            decor_name (str): Decoration name
            x (int): X position
            y (int): Y position
            
        Returns:
            None
        """
        if self.level_script.is_room():
            self.level_script.room().add_decor_by_name(decor_name, x, y)
        return None
    
    def _script_add_goal(self, script_state, goal_name, codename):
        """
        Add a goal from Lua script.
        
        Args:
            script_state: Script state
            goal_name (str): Goal name
            codename (str): Level codename
            
        Returns:
            None
        """
        if self.level_script.is_room():
            self.level_script.room().add_goal(goal_name, codename)
        return None
    
    def _script_add_rules(self, script_state, rules_str):
        """
        Add rules from Lua script.
        
        Args:
            script_state: Script state
            rules_str (str): Rules string
            
        Returns:
            None
        """
        if self.level_script.is_room():
            self.level_script.room().add_rules(rules_str)
        return None
    
    def _script_save(self, script_state):
        """
        Save the game from Lua script.
        
        Args:
            script_state: Script state
            
        Returns:
            None
        """
        if self.level_script.is_room():
            models = self.level_script.room().get_models_state()
            self.save_game(models)
        return None
    
    def _script_load(self, script_state):
        """
        Load the game from Lua script.
        
        Args:
            script_state: Script state
            
        Returns:
            None
        """
        if 'saved_moves' in script_state.state.globals():
            self.load_game(script_state.state.globals()['saved_moves'])
        return None
    
    def _script_save_undo(self, script_state, old_moves, keep_last):
        """
        Save undo state from Lua script.
        
        Args:
            script_state: Script state
            old_moves (str): Old moves
            keep_last (bool): Whether to keep the last move
            
        Returns:
            None
        """
        # Save current state for undo
        if self.level_script.is_room():
            # Get room state
            room = self.level_script.room()
            models_state = room.get_models_state()
            
            # Save to undo file
            undo_file = Path.data_write_path(f"undo/{self.codename}.lua")
            try:
                # Ensure directory exists
                import os
                os.makedirs(os.path.dirname(undo_file.get_native()), exist_ok=True)
                
                with open(undo_file.get_native(), 'w') as f:
                    f.write(f"undo_moves = '{old_moves}'\n")
                    f.write(f"undo_models = {models_state}\n")
                    f.write(f"undo_keep_last = {str(keep_last).lower()}\n")
                
                # log_debug(f"Saved undo state to {undo_file.get_native()}")
            except Exception as e:
                log_warning(f"Failed to save undo state: {e}")
        
        return None
    
    def _script_load_undo(self, script_state, moves, steps):
        """
        Load undo state from Lua script.
        
        Args:
            script_state: Script state
            moves (str): Moves to load
            steps (int): Number of steps
            
        Returns:
            None
        """
        # Load undo state
        if self.level_script.is_room():
            # Determine which state to load
            if steps > 0:  # Undo
                # We need to truncate moves to eliminate the last 'steps' moves
                if len(moves) >= steps:
                    new_moves = moves[:-steps]
                    # Load the state and apply new moves
                    room = self.level_script.room()
                    room.set_moves(new_moves)
                    self.undo_steps = 0
            elif steps < 0:  # Redo
                # We need to load the next state (not implemented yet)
                pass
            
            # Indicate that we've completed this undo action
            self.action_undo_finish()
        
        return None
    
    def _script_load_final_undo(self, script_state):
        """
        Load final undo state from Lua script.
        
        Args:
            script_state: Script state
            
        Returns:
            None
        """
        # Load the undo file and apply state
        undo_file = Path.data_read_path(f"undo/{self.codename}.lua")
        if Path.exists(undo_file):
            try:
                # Execute the undo file to get variables
                self.script_include(undo_file)
                
                # Get undo state from lua globals
                undo_moves = script_state.get_global("undo_moves")
                undo_models = script_state.get_global("undo_models")
                
                # Apply to the room
                if self.level_script.is_room() and undo_moves and undo_models:
                    room = self.level_script.room()
                    room.set_moves(undo_moves)
                    room.set_models_state(undo_models)
                    # log_debug(f"Loaded undo state with moves: {undo_moves}")
            except Exception as e:
                log_warning(f"Failed to load undo state: {e}")
        
        return None
    
    def _script_save_state(self, script_state):
        """
        Save game state from Lua script.
        
        Args:
            script_state: Script state
            
        Returns:
            None
        """
        # Save the current game state for loading after a move
        if self.level_script.is_room():
            # Get the current state
            room = self.level_script.room()
            models_state = room.get_models_state()
            moves = room.step_counter().get_moves()
            
            # Write to a temporary file
            state_file = Path.data_write_path(f"state/{self.codename}_temp.lua")
            try:
                # Ensure directory exists
                import os
                os.makedirs(os.path.dirname(state_file.get_native()), exist_ok=True)
                
                with open(state_file.get_native(), 'w') as f:
                    f.write(f"state_moves = '{moves}'\n")
                    f.write(f"state_models = {models_state}\n")
                
                # log_debug(f"Saved game state to {state_file.get_native()}")
            except Exception as e:
                log_warning(f"Failed to save game state: {e}")
        
        return None
    
    def _script_load_state(self, script_state):
        """
        Load game state from Lua script.
        
        Args:
            script_state: Script state
            
        Returns:
            None
        """
        # Load the temporary game state after a move
        if self.level_script.is_room():
            state_file = Path.data_read_path(f"state/{self.codename}_temp.lua")
            if Path.exists(state_file):
                try:
                    # Execute the state file to get variables
                    self.script_include(state_file)
                    
                    # Get state from lua globals
                    state_moves = script_state.get_global("state_moves")
                    state_models = script_state.get_global("state_models")
                    
                    # Apply to the room
                    if state_moves and state_models:
                        room = self.level_script.room()
                        room.set_moves(state_moves)
                        room.set_models_state(state_models)
                        # log_debug(f"Loaded game state with moves: {state_moves}")
                except Exception as e:
                    log_warning(f"Failed to load game state: {e}")
        
        return None
    
    def own_init_state(self) -> None:
        """Start gameplay. fill_desc() and fill_status() must be called before."""
        if self.desc is None:
            raise LogicException(ExInfo("level description is NULL")
                                .add_info("codename", self.codename))
        
        self.countdown.reset()
        self.loading.reset()
        
        # Let level first draw and then play
        self.locker.reset()
        self.locker.ensure_phases(1)
        
        # Stop music if not undoing
        if not self.is_undoing():
            SoundAgent.agent().stop_music()
        
        self.script_do(f'CODENAME = [[{self.codename}]]')
        self.script_include(self.datafile)
        if self.pending_replay_moves is not None:
            moves = self.pending_replay_moves
            self.pending_replay_moves = None
            self.loading.load_replay(moves)
        log_debug(f"Successfully loaded Lua script for level: {self.codename}")
    
    def own_update_state(self) -> None:
        """Update level."""
        self.new_round = False
        if self.locker.get_locked() == 0:
            self.new_round = True
            self.next_action()
        
        self.update_level()
        self.locker.dec_lock()
        
        if self.countdown.count_down(self):
            self.finish_level()
    
    def own_pause_state(self) -> None:
        """Pause level."""
        self.level_script.kill_plan()
        self.action_undo_finish()
    
    def own_resume_state(self) -> None:
        """Resume level."""
        if self.level_script.is_room():
            self.init_screen()
    
    def own_clean_state(self) -> None:
        """Clean room after visit."""
        self.level_script.clean_room()
    
    def own_note_bg(self) -> None:
        """Loading is paused on background."""
        if self.loading.is_loading() and not self.loading.is_paused():
            self.loading.toggle_pause()
        self.action_undo_finish()
    
    def own_note_fg(self) -> None:
        """Resume loading on foreground."""
        self.init_screen()
        if self.loading.is_loading() and self.loading.is_paused():
            self.loading.toggle_pause()
        
        # Ensure that an unwanted mouse press will not move a fish
        self.locker.ensure_phases(3)
    
    def is_undoing(self) -> bool:
        """Check if level is undoing."""
        return self.undo_steps != 0
    
    def is_acting(self) -> bool:
        """Check if level is acting."""
        return self.is_showing() or self.is_loading() or self.is_undoing()
    
    def is_loading(self) -> bool:
        """Check if level is loading."""
        return self.loading.is_loading()
    
    def toggle_pause(self) -> None:
        """Toggle pause state."""
        return self.loading.toggle_pause()
    
    def next_action(self) -> None:
        """Process next action."""
        if self.is_undoing():
            self.next_undo_action()
        elif self.is_loading():
            self.next_load_action()
        elif self.is_showing():
            self.next_show_action()
        else:
            self.next_player_action()
    
    def update_level(self) -> None:
        """Update level (plan dialogs, do anim, ...)."""
        if not self.is_undoing() and not self.is_loading():
            self.level_script.update_script()
    
    def save_undo(self, old_moves: str) -> None:
        """
        Save state for undo.
        Should be called after a player move, but still before level script update.
        
        Args:
            old_moves: Moves before the last move
        """
        if self.level_script.is_room():
            room = self.level_script.room()
            keep_last = self.was_dangerous_move
            self.was_dangerous_move = room.step_counter().is_dangerous_move()
            
            keep_last_value = "true" if keep_last else "false"
            self.script_do(f'script_saveUndo("{old_moves}", {keep_last_value})')
    
    def finish_level(self) -> None:
        """
        Finish complete level.
        Save solution.
        """
        if self.countdown.is_finished_enough():
            self.countdown.save_solution()
            next_state = self.countdown.create_next_state()
            if next_state:
                self.change_state(next_state)
            else:
                self.quit_state()
        elif self.countdown.is_wrong_enough():
            self.action_restart(1)
    
    def next_player_action(self) -> None:
        """
        Update room.
        Let objects move.
        """
        if self.level_script.is_room():
            room = self.level_script.room()
            old_moves = room.step_counter().get_moves()
            room.next_round(self.get_input())
            
            # The old positions are now occupied, so check if it's solvable
            was_solvable = room.is_solvable()
            self.was_dangerous_move = self.was_dangerous_move or room.is_falling()
            
            if was_solvable and not room.is_falling():
                self.save_undo(old_moves)
    
    def save_game(self, models: str) -> None:
        """
        Write save to the file.
        Save moves and models state.
        
        Args:
            models: Saved models
        """
        if self.level_script.is_room():
            file_path = Path.data_write_path(f"saves/{self.codename}.lua")
            try:
                with open(file_path.get_native(), 'w') as save_file:
                    moves = self.level_script.room().step_counter().get_moves()
                    save_file.write(f"\nsaved_moves = '{moves}'\n")
                    save_file.write(f"\nsaved_models = {models}")
                self.display_save_status()
            except Exception as e:
                log_warning(ExInfo("cannot save game")
                           .add_info("file", file_path.get_native())
                           .add_info("error", str(e)))
    
    def display_save_status(self) -> None:
        """Display save status."""
        TIME = 3
        log_info(ExInfo("game is saved")
                .add_info("codename", self.codename))
        from effect.picture import Picture  # Import here to avoid circular imports
        self.status_display.display_status(
            Picture(Path.data_read_path("images/menu/status/saved.png"), V2(0, 0)), TIME)
    
    def load_game(self, moves: str) -> None:
        """
        Start loading mode.
        
        Args:
            moves: Saved moves to load
        """
        if self.is_undoing():
            if self.level_script.is_room():
                self.level_script.room().set_moves(moves)
        else:
            self.loading.load_game(moves)
    
    def load_replay(self, moves: str) -> None:
        """
        Start replay mode.
        
        Args:
            moves: Saved moves to load
        """
        if self.is_running():
            self.loading.load_replay(moves)
        else:
            self.pending_replay_moves = moves
    
    def next_load_action(self) -> None:
        """Load next move."""
        self.loading.next_load_action()
        if not self.is_loading():
            self.script_do("script_loadState()")
    
    def next_show_action(self) -> None:
        """Let show execute."""
        if self.level_script.is_room():
            self.level_script.room().begin_fall()
            self.show.execute_first()
            self.level_script.room().finish_round()
    
    def next_undo_action(self) -> None:
        """Do the next undo step."""
        if self.level_script.is_room():
            moves = self.level_script.room().step_counter().get_moves()
            self.script_do(f'script_loadUndo("{moves}", {self.undo_steps})')
    
    def action_restart(self, increment: int) -> bool:
        """
        (re)start room.
        
        Args:
            increment: Increment restart counter by this value
            
        Returns:
            bool: True
        """
        if increment > 0:
            self.undo_steps = 0
        
        self.own_clean_state()
        self.restart_counter += increment
        # The script is just overridden by itself,
        # so planned shows and undo remain after restart
        self.own_init_state()
        return True
    
    def action_move(self, symbol: str) -> bool:
        """
        Move a fish.
        
        Args:
            symbol: Move symbol, e.g. 'U', 'D', 'L', 'R'
            
        Returns:
            bool: True when move is done
        """
        return self.level_script.room().make_move(symbol)
    
    def action_save(self) -> bool:
        """
        Save position.
        
        Returns:
            bool: True
        """
        if self.level_script.room().is_solvable():
            self.script_do("script_save()")
        else:
            log_info(ExInfo("bad level condition, level cannot be finished, no save is made"))
        return True
    
    def action_load(self) -> bool:
        """
        Load position.
        
        Returns:
            bool: True
        """
        file_path = Path.data_read_path(f"saves/{self.codename}.lua")
        if file_path.exists():
            self.undo_steps = 0
            self.restart_counter -= 1
            self.action_restart(1)
            self.script_include(file_path)
            self.script_do("script_load()")
        else:
            log_info(ExInfo("there is no file to load")
                    .add_info("file", file_path.get_native()))
        return True
    
    def action_undo(self, steps: int) -> None:
        """
        Start the undoing.
        
        Args:
            steps: 1 for undo, -1 for redo
        """
        self.undo_steps = steps
        self.level_script.kill_plan()
        self.countdown.reset()
        self.next_undo_action()
    
    def action_undo_finish(self) -> None:
        """Restart the room at the current undo position."""
        if not self.is_undoing():
            return
        
        self.action_restart(0)
        self.script_do("script_loadFinalUndo()")
        self.undo_steps = 0
    
    def switch_fish(self) -> None:
        """Switch the active fish."""
        if self.level_script.is_room():
            self.level_script.room().switch_fish()
    
    def control_event(self, stroke) -> None:
        """
        Handle a key control event.
        
        Args:
            stroke: The key stroke
        """
        if self.level_script.is_room():
            self.level_script.room().control_event(stroke)
    
    def control_mouse(self, button) -> None:
        """
        Handle a mouse control event.
        
        Args:
            button: The mouse button
        """
        if self.level_script.is_room():
            self.level_script.room().control_mouse(button)
    
    def create_room(self, w: int, h: int, picture: str) -> None:
        """
        Create new room and change screen resolution.
        
        Args:
            w: Room width
            h: Room height
            picture: Room background picture
        """
        from level.step_decor import StepDecor  # Import here to avoid circular imports
        from level.room import Room  # Import here to avoid circular imports
        
        room = Room(w, h, picture, self.locker, self.level_script)
        room.add_decor(StepDecor(room.step_counter()))
        self.level_script.take_room(room)
        self.background.remove_all()
        self.background.accept_drawer(room)
        
        self.init_screen()
    
    def init_screen(self) -> None:
        """Initialize screen for the level."""
        if self.level_script.is_room():
            title = f"{self.codename}"
            if self.desc:
                level_name = self.desc.find_level_name(self.codename)
                level_desc = self.desc.find_desc(self.codename)
                if level_name and level_desc:
                    title = f"{level_desc}: {level_name}"
                elif level_name:
                    title = level_name
            
            from gengine.agent.option_agent import OptionAgent
            from gengine.agent.video_agent import VideoAgent
            from level.view import View
            
            options = OptionAgent.agent()
            options.set_param("caption", title)
            options.set_param("screen_width", 
                             self.level_script.room().get_w() * View.SCALE)
            options.set_param("screen_height",
                             self.level_script.room().get_h() * View.SCALE)
            VideoAgent.agent().init_video_mode()
    
    def new_demo(self, demofile: Path) -> None:
        """
        Create and show a demo.
        
        Args:
            demofile: Path to demo file
        """
        from state.demo_mode import DemoMode  # Import here to avoid circular imports
        
        self.level_script.interrupt_plan()
        demo = DemoMode(demofile)
        self.push_state(demo)
    
    def is_showing(self) -> bool:
        """
        Check if the level is showing an animation.
        
        Returns:
            bool: True if showing
        """
        return not self.show.empty()
    
    def interrupt_show(self) -> None:
        """Interrupt current show."""
        self.show.remove_all()
    
    def plan_show(self, new_command) -> None:
        """
        Plan a command to show.
        
        Args:
            new_command: Command to show
        """
        self.show.plan_command(new_command)
        
    def draw_on(self, screen) -> None:
        """
        Draw the level on the screen.
        
        Args:
            screen: The screen to draw on
        """
        # Draw the background drawer which contains the room
        self.background.draw_on(screen)
        self.level_script.get_subtitle_agent().draw_on(screen)
        self.status_display.draw_on(screen)
    
    def get_level_name(self) -> str:
        """
        Get the level name.
        
        Returns:
            str: Level name
        """
        return self.desc.find_level_name(self.codename)
    
    def get_restart_counter(self) -> int:
        """
        Get the restart counter.
        
        Returns:
            int: Restart counter
        """
        return self.restart_counter
    
    def get_depth(self) -> int:
        """
        Get the level depth.
        
        Returns:
            int: Level depth
        """
        return self.depth
    
    def is_new_round(self) -> bool:
        """
        Check if this is a new round.
        
        Returns:
            bool: True if new round
        """
        return self.new_round
    
    def get_count_for_solved(self) -> int:
        """
        Get the countdown for solved levels.
        
        Returns:
            int: Countdown value
        """
        countdown = 10
        if self.is_undoing():
            countdown = -1
        elif self.is_loading():
            countdown = 0
        elif self.level_script.dialogs().are_running():
            countdown = 30
        return countdown
    
    def get_count_for_wrong(self) -> int:
        """
        Get the countdown for wrong levels.
        
        Returns:
            int: Countdown value (75)
        """
        return 75
