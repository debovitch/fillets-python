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

from gengine.log import log_debug, log_info
from gengine.ex_info import ExInfo
from level.dir import Dir
from level.control_sym import ControlSym
from level.key_control import KeyControl
from level.cube import Cube
from gengine.key_stroke import KeyStroke

class Unit:
    """
    Driver for model (player representation).
    """
    
    def __init__(self, key_control, control_sym, start_active=False):
        """
        Initialize a unit with controls.
        
        Args:
            key_control (KeyControl): Keyboard control mapping
            control_sym (ControlSym): Control symbols for move recording
            start_active (bool): Whether this unit is active at start
        """
        self.key_control = key_control
        self.control_sym = control_sym
        self.start_active_flag = start_active
        self.model = None
        self.dir = Dir.DIR_NO
    
    def take_model(self, model):
        """
        Set the model this unit controls.
        
        Args:
            model: The model to control
        """
        self.model = model
    
    def get_model(self):
        """
        Get the model this unit controls.
        
        Returns:
            The model
        """
        return self.model
    
    def start_active(self):
        """
        Whether this unit should be active at start.
        
        Returns:
            bool: True if this unit should be active at start
        """
        return self.start_active_flag
    
    def can_drive(self):
        """
        Whether this unit can be driven.
        
        Returns:
            bool: True if this unit can be driven
        """
        return (self.model and self.model.is_alive()
                and not self.model.is_lost()
                and not self.model.is_busy())
    
    def drive(self, input_provider):
        """
        Test keys and try to move with this unit's own controls.
        
        Args:
            input_provider: The input provider
            
        Returns:
            str: Move symbol or SYM_NONE
        """
        return self.drive_borrowed(input_provider, self.key_control)

    def drive_borrowed(self, input_provider, key_control):
        """
        Test keys and try to move with borrowed controls.
        """
        if not self.can_drive() or input_provider is None:
            return ControlSym.SYM_NONE

        if input_provider.is_pressed(key_control.get_left()):
            return self.go_left()
        if input_provider.is_pressed(key_control.get_right()):
            return self.go_right()
        if input_provider.is_pressed(key_control.get_up()):
            return self.go_up()
        if input_provider.is_pressed(key_control.get_down()):
            return self.go_down()

        return ControlSym.SYM_NONE

    def activate(self):
        """Greet the player by scheduling the activation action."""
        if self.model:
            self.model.get_rules().action_activate()

    def my_symbol(self, key):
        """Translate this key to this unit's move symbol."""
        return self.my_symbol_borrowed(key, self.key_control)

    def my_symbol_borrowed(self, key, key_control):
        """Translate this key using borrowed key bindings."""
        if key == key_control.get_left():
            return self.control_sym.get_left()
        if key == key_control.get_right():
            return self.control_sym.get_right()
        if key == key_control.get_up():
            return self.control_sym.get_up()
        if key == key_control.get_down():
            return self.control_sym.get_down()
        return ControlSym.SYM_NONE

    def my_order(self, direction):
        """Return this unit's saved move symbol for a direction."""
        if direction == Dir.DIR_LEFT:
            return self.control_sym.get_left()
        if direction == Dir.DIR_RIGHT:
            return self.control_sym.get_right()
        if direction == Dir.DIR_UP:
            return self.control_sym.get_up()
        if direction == Dir.DIR_DOWN:
            return self.control_sym.get_down()
        return ControlSym.SYM_NONE
    
    def drive_order(self, move):
        """
        Try to drive model.
        
        Args:
            move (str): Move command ('u', 'd', 'l', 'r', 'U', 'D', 'L', 'R')
            
        Returns:
            str: Move if the move was successful, empty string otherwise
        """
        if not self.can_drive():
            return ControlSym.SYM_NONE

        if self.control_sym.get_left() == move:
            return self.go_left()
        if self.control_sym.get_right() == move:
            return self.go_right()
        if self.control_sym.get_up() == move:
            return self.go_up()
        if self.control_sym.get_down() == move:
            return self.go_down()

        return ControlSym.SYM_NONE

    def go_left(self):
        symbol = ControlSym.SYM_NONE
        if self.model.is_left():
            if self.model.get_rules().action_move_dir(Dir.DIR_LEFT):
                symbol = self.control_sym.get_left()
        else:
            self.model.get_rules().action_turn_side()
            symbol = self.control_sym.get_left()
        return symbol

    def go_right(self):
        symbol = ControlSym.SYM_NONE
        if not self.model.is_left():
            if self.model.get_rules().action_move_dir(Dir.DIR_RIGHT):
                symbol = self.control_sym.get_right()
        else:
            self.model.get_rules().action_turn_side()
            symbol = self.control_sym.get_right()
        return symbol

    def go_up(self):
        if self.model.get_rules().action_move_dir(Dir.DIR_UP):
            return self.control_sym.get_up()
        return ControlSym.SYM_NONE

    def go_down(self):
        if self.model.get_rules().action_move_dir(Dir.DIR_DOWN):
            return self.control_sym.get_down()
        return ControlSym.SYM_NONE
    
    def will_move(self):
        """
        Whether this unit will be able to move.
        
        Returns:
            bool: True if this unit will be able to move
        """
        return self.model and self.model.is_alive() and not self.model.is_lost()
    
    def is_powerful(self):
        """
        Whether this unit is powerful.
        
        Returns:
            bool: True if this unit is powerful
        """
        return self.model and self.model.get_power().value >= Cube.Weight.HEAVY.value
    
    def is_pushing(self):
        """
        Whether this unit is pushing.
        
        Returns:
            bool: True if this unit is pushing
        """
        return self.model and self.model.get_rules().is_pushing()

    def is_moving(self):
        """Whether the unit is currently moving or turning."""
        if not self.can_drive():
            return False
        action = self.model.get_rules().get_action()
        return action in ("move_left", "move_right", "move_up", "move_down", "turn")

    def is_moving_down(self):
        """Whether the unit's current move direction is down."""
        return self.model and self.model.get_rules().get_dir() == Dir.DIR_DOWN

    def is_turning(self):
        """Whether the unit is turning."""
        return self.model and self.model.get_rules().get_action() == "turn"

    def is_driven_by(self, symbol):
        """Whether this move symbol belongs to this unit."""
        return symbol in (
            self.control_sym.get_left(),
            self.control_sym.get_right(),
            self.control_sym.get_up(),
            self.control_sym.get_down(),
        )

    def equals_model(self, other):
        """Whether this unit controls the given model."""
        return self.model is other

    def get_loc(self):
        return self.model.get_location()

    def get_w(self):
        return self.model.get_shape().get_w()

    def get_h(self):
        return self.model.get_shape().get_h()

    def is_free_place(self, loc):
        return self.model.get_rules().is_free_place(loc)

    def count_anim_phases(self, anim):
        return self.model.anim.count_anim_phases(anim)
