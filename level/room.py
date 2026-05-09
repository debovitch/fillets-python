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

from gengine.drawable import Drawable
from level.cube import Cube
from level.dir import Dir
from level.field import Field
from gengine.v2 import V2
from gengine.resource.res_sound_pack import ResSoundPack
from gengine.path import Path
from gengine.agent.sound_agent import SoundAgent
from gengine.agent.option_agent import OptionAgent
from gengine.agent.timer_agent import TimerAgent
from effect.wavy_picture import WavyPicture

class Room(Drawable):
    """
    Room with level.
    Contains the game field, models, controls, and game state.
    """
    
    def __init__(self, w, h, picture, locker, level_script):
        """
        Create room holder.
        
        Args:
            w (int): Room width
            h (int): Room height
            picture (str): Room background
            locker: Shared locker for animation
            level_script: Shared planner to interrupt
        """
        self.locker = locker
        self.level_script = level_script
        self.fast_falling = False
        self.bg = WavyPicture(Path.data_read_path(picture), V2(0, 0))
        self.bg_filename = picture
        self.field = Field(w, h)
        from level.finder_alg import FinderAlg
        self.finder = FinderAlg(w, h)
        self.controls = None
        self.view = None
        self.models = []
        self.last_action = Cube.Action.ACTION_NO
        self.sound_pack = ResSoundPack()
        self.start_time = TimerAgent.agent().get_cycles()

        from level.controls import Controls
        self.controls = Controls(locker)
        from level.view import View
        from level.model_list import ModelList
        self.view = View(ModelList(self.models), w, h)

    def __del__(self):
        """
        Delete field and models.
        Clean up resources when the object is deleted.
        """
        self.clean()

    def clean(self):
        """Release resources owned by the room."""
        if getattr(self, "sound_pack", None):
            self.sound_pack.remove_all()
            self.sound_pack = None

        if getattr(self, "level_script", None):
            self.level_script.kill_plan()
            self.level_script.dialogs().remove_all()
            from plan.subtitle_agent import SubTitleAgent
            SubTitleAgent.get_instance().remove_all()

        for model in getattr(self, "models", []):
            if model:
                model.clean()
        self.models.clear()

        self.controls = None
        self.view = None
        self.finder = None
        self.field = None
        self.bg = None
    
    def set_waves(self, amplitude, periode, speed):
        """
        Set waves on background.
        
        Args:
            amplitude (float): Wave amplitude
            periode (float): Wave period
            speed (float): Wave speed
        """
        self.bg.set_wamp(amplitude)
        self.bg.set_wperiode(periode)
        self.bg.set_wspeed(speed)
    
    def add_decor(self, new_decor):
        """
        Add decoration to the room.
        
        Args:
            new_decor: New decoration object
        """
        self.view.add_decor(new_decor)
    
    def set_fast_falling(self, value):
        """
        Set whether objects should fall quickly.
        
        Args:
            value (bool): Whether objects should fall quickly
        """
        self.fast_falling = value
    
    def add_model(self, new_model, new_unit):
        """
        Add model to the scene.
        
        Args:
            new_model (Cube): New object
            new_unit: Driver for the object or None
            
        Returns:
            int: Model index
        """
        # Create rules if needed
        new_model.create_rules()
        # Connect model with field
        new_model.get_rules().take_field(self.field)
        self.models.append(new_model)
        
        if new_unit:
            new_unit.take_model(new_model)
            self.controls.add_unit(new_unit)
        
        model_index = len(self.models) - 1
        new_model.set_index(model_index)
        return model_index
    
    def get_model(self, model_index):
        """
        Return model at index.
        
        Args:
            model_index (int): The index of the model
            
        Returns:
            Cube: The model at the index
            
        Raises:
            Exception: If model_index is out of range
        """
        if 0 <= model_index < len(self.models):
            return self.models[model_index]
        else:
            from gengine.exceptions import LogicException
            from gengine.ex_info import ExInfo
            raise LogicException(ExInfo(f"Bad model index: {model_index}"))
    
    def ask_field(self, loc):
        """
        Return model at location.
        
        Args:
            loc (V2): The location
            
        Returns:
            Cube: The model at the location
        """
        return self.field.get_model(loc)
    
    def next_round(self, input_provider):
        """
        Update all models.
        Prepare new move, let models fall, let models drive, release old position.
        
        Args:
            input_provider: The input provider
        """
        if self.fast_falling:
            while self.begin_fall():
                self.finish_round()
        else:
            self.begin_fall()
        
        if self.is_fresh():
            if input_provider and hasattr(self.controls, 'driving'):
                if self.controls.driving(input_provider):
                    self.last_action = Cube.Action.ACTION_MOVE
                elif self.mouse_drive(input_provider):
                    self.last_action = Cube.Action.ACTION_MOVE
        
        self.finish_round()
    
    def play_impact(self, impact):
        """
        Play sound like some object has fallen.
        Only one sound is played even if more objects have fallen.
        
        Args:
            impact (Cube.Weight): The impact weight
        """
        if impact == Cube.Weight.NONE:
            pass
        elif impact == Cube.Weight.LIGHT:
            self.play_sound("impact_light", 50)
        elif impact == Cube.Weight.HEAVY:
            self.play_sound("impact_heavy", 50)
        else:
            assert False, "Unknown impact weight"
    
    def play_dead(self, model):
        """
        Play sound like a fish died.
        
        Args:
            model (Cube): Fresh dead fish
        """
        if hasattr(self.level_script, 'dialogs') and callable(self.level_script.dialogs):
            dialogs = self.level_script.dialogs()
            if hasattr(dialogs, 'kill_sound'):
                dialogs.kill_sound(model.get_index())
        
        if model.get_power() == Cube.Weight.LIGHT:
            self.play_sound("dead_small")
        elif model.get_power() == Cube.Weight.HEAVY:
            self.play_sound("dead_big")
    
    def prepare_round(self):
        """
        Move all models to new position and check dead fishes.
        """
        interrupt = False

        for model in self.models:
            model.get_rules().free_old_pos()
        for model in self.models:
            model.get_rules().occupy_new_pos()
        for model in self.models:
            die = model.get_rules().check_dead(self.last_action)
            interrupt = interrupt or die
            if die:
                self.play_dead(model)
        for model in self.models:
            model.get_rules().change_state()

        if interrupt:
            self.level_script.interrupt_plan()
    
    def fallout(self, interactive=True):
        """
        Let models go out of screen.
        
        Args:
            interactive (bool): Whether to do animation
            
        Returns:
            bool: True when a model went out
        """
        went_out = False
        for model in self.models:
            if model.is_lost():
                continue
            out_depth = model.get_rules().action_out()
            if out_depth > 0:
                went_out = True
                if interactive:
                    self.locker.ensure_phases(3)
            elif out_depth == -1:
                self.level_script.interrupt_plan()

        return went_out
    
    def falldown(self, interactive=True):
        """
        Let things fall.
        
        Args:
            interactive (bool): Whether to do animation
            
        Returns:
            bool: True when something is falling
        """
        from level.landslip import Landslip
        from level.model_list import ModelList
        
        models = ModelList(self.models)
        slip = Landslip(models)
        
        falling = slip.compute_fall()
        if interactive and falling:
            self.play_impact(slip.get_impact())
        return falling
    
    def finish_round(self, interactive=True):
        """
        Let models release their old position.
        
        Args:
            interactive (bool): Whether to ensure phases for motion animation
        """
        if interactive and hasattr(self.controls, 'lock_phases'):
            self.controls.lock_phases()
        
        self.view.note_new_round(self.locker.get_locked())
    
    def begin_fall(self, interactive=True):
        """
        Begin round. Let objects fall.
        First objects can fall out of room (even upward),
        when nothing is going out, then objects can fall down by gravity.
        
        Args:
            interactive (bool): Whether to play sound and do animation
            
        Returns:
            bool: True when something was falling
        """
        self.prepare_round()
        self.last_action = Cube.Action.ACTION_NO
        
        if self.fallout(interactive):
            self.last_action = Cube.Action.ACTION_MOVE
        else:
            if self.falldown(interactive):
                self.last_action = Cube.Action.ACTION_FALL
        
        return self.last_action != Cube.Action.ACTION_NO
    
    def switch_fish(self):
        """
        Switch active fish.
        """
        if hasattr(self.controls, 'switch_active'):
            self.controls.switch_active()
    
    def control_event(self, stroke):
        """
        Handle control event.
        
        Args:
            stroke: The keystroke
        """
        if hasattr(self.controls, 'control_event'):
            self.controls.control_event(stroke)
    
    def control_mouse(self, button):
        """
        Handle mouse control event.
        
        Args:
            button: The mouse button
        """
        if hasattr(button, "is_left") and button.is_left():
            field_pos = self.view.get_field_pos(button.get_loc())
            self.controls.activate_selected(self.ask_field(field_pos))

    def mouse_drive(self, input_provider):
        """
        Drive the active unit from mouse state.

        Left button follows a shortest path without pushing. Right button moves
        directly toward the cursor, allowing pushes.
        """
        field = self.view.get_field_pos(input_provider.get_mouse_loc())
        if input_provider.is_left_pressed():
            return self.move_to(field)
        if input_provider.is_right_pressed():
            return self.move_hard_to(field)
        return False

    def move_to(self, field):
        """Move along the shortest path without pushing."""
        unit = self.controls.get_active()
        if not unit:
            return False

        direction = self.finder.find_dir(unit, field)
        if direction != Dir.DIR_NO:
            return self.controls.make_move(unit.my_order(direction))
        return False

    def move_hard_to(self, field):
        """Move directly toward the cursor."""
        unit = self.controls.get_active()
        if not unit:
            return False

        loc = unit.get_loc()
        if field.get_x() < loc.get_x():
            return self.controls.make_move(unit.my_order(Dir.DIR_LEFT))
        if loc.get_x() + unit.get_w() <= field.get_x():
            return self.controls.make_move(unit.my_order(Dir.DIR_RIGHT))
        if field.get_y() < loc.get_y():
            return self.controls.make_move(unit.my_order(Dir.DIR_UP))
        if loc.get_y() + unit.get_h() <= field.get_y():
            return self.controls.make_move(unit.my_order(Dir.DIR_DOWN))
        return False
    
    def load_move(self, move):
        """
        Load this move, let object fall fast.
        Don't play sound.
        
        Args:
            move (char): The move character
            
        Raises:
            Exception: For bad moves
        """
        NO_INTERACTIVE = False
        falling = True
        
        while falling:
            falling = self.begin_fall(NO_INTERACTIVE)
            self.make_move(move)
            self.finish_round(NO_INTERACTIVE)
    
    def make_move(self, move):
        """
        Try to make single move.
        
        Args:
            move (char): The move character
            
        Returns:
            bool: True for success or False when something has moved before
            
        Raises:
            Exception: For bad moves
        """
        result = False
        
        if self.is_fresh():
            if hasattr(self.controls, 'make_move'):
                if not self.controls.make_move(move):
                    from gengine.exceptions import LogicException
                    from gengine.ex_info import ExInfo
                    raise LogicException(ExInfo(f"Load error - bad move: {move}"))
                
                self.last_action = Cube.Action.ACTION_MOVE
                result = True
        
        return result
    
    def cannot_move(self):
        """
        Returns true when there is no unit which will be able to move.
        
        Returns:
            bool: True when no unit can move
        """
        if hasattr(self.controls, 'cannot_move'):
            return self.controls.cannot_move()
        return False
    
    def is_solvable(self):
        """
        Returns true when all goals can be solved.
        
        Returns:
            bool: True when all goals can be solved
        """
        for model in self.models:
            if model.is_wrong():
                return False
        
        return True
    
    def is_solved(self):
        """
        Returns true when all goals are satisfied.
        Right time to ask is after finish_round.
        Room is not solved when something is still falling.
        
        Returns:
            bool: True when all goals are satisfied
        """
        if not self.is_fresh():
            return False
        
        for model in self.models:
            if not model.is_satisfy():
                return False
        
        return True
    
    def is_falling(self):
        """
        Check if something is falling.
        
        Returns:
            bool: True when something is falling
        """
        return self.last_action == Cube.Action.ACTION_FALL
    
    def is_fresh(self):
        """
        Check if the room is in a fresh state (no action).
        
        Returns:
            bool: True when in fresh state
        """
        return self.last_action == Cube.Action.ACTION_NO
    
    def check_active(self):
        """
        Check if active unit is valid.
        """
        if hasattr(self.controls, 'check_active'):
            self.controls.check_active()
    
    def unbusy_units(self):
        """
        Mark all units as not busy.
        """
        for model in self.models:
            if hasattr(model, 'set_busy'):
                model.set_busy(False)
    
    def step_counter(self):
        """
        Get the step counter.
        
        Returns:
            The step counter
        """
        return self.controls
    
    def set_moves(self, moves):
        """
        Set the moves.
        
        Args:
            moves (str): The moves
        """
        if hasattr(self.controls, 'set_moves'):
            self.controls.set_moves(moves)
    
    def get_w(self):
        """
        Get the width of the room.
        
        Returns:
            int: The width
        """
        return self.field.get_w()
    
    def get_h(self):
        """
        Get the height of the room.
        
        Returns:
            int: The height
        """
        return self.field.get_h()
    
    def get_cycles(self):
        """
        Get the number of cycles elapsed.
        
        Returns:
            int: The number of cycles
        """
        return TimerAgent.agent().get_cycles() - self.start_time
    
    def add_sound(self, name, file):
        """
        Add sound to the sound pack.
        
        Args:
            name (str): The name of the sound
            file (Path): The sound file
        """
        self.sound_pack.add_sound(name, file)
    
    def play_sound(self, name, volume=100):
        """
        Play a sound.
        
        Args:
            name (str): The name of the sound
            volume (int): The volume (0-100)
        """
        if OptionAgent.agent().get_as_bool("sound", True):
            SoundAgent.agent().play_sound(
                self.sound_pack.get_random_res(name), volume)
    
    def set_screen_shift(self, shift):
        """
        Shift room content.
        Note: background is not shifted.
        
        Args:
            shift (V2): The shift
        """
        self.view.set_screen_shift(shift)
    
    def change_bg(self, picture):
        """
        Change the background.
        
        Args:
            picture (str): The new background
        """
        if picture != self.bg_filename:
            self.bg.change_picture(Path.data_read_path(picture))
            self.bg_filename = picture
    
    def get_bg(self):
        """
        Get the background filename.
        
        Returns:
            str: The background filename
        """
        return self.bg_filename
    
    def draw_on(self, screen):
        """
        Draw the room on the screen.
        
        Args:
            screen: The screen to draw on
        """
        self.bg.draw_on(screen)
        self.view.draw_on(screen)
