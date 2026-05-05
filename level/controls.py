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

from level.step_counter import StepCounter
from level.control_sym import ControlSym
from level.key_control import KeyControl


class Controls(StepCounter):
    """
    Keyboard and mouse controls.
    Implements the StepCounter interface to track moves.
    """

    def __init__(self, phase_locker=None):
        """
        Create list of drivers.

        Args:
            phase_locker: Shared locker for animation
        """
        self.units = []
        self.active_index = 0
        self.speedup = 0
        self.arrows = KeyControl()
        self.switch = True
        self.moves = ""
        self.locker = phase_locker
        self.stroke_symbol = ControlSym.SYM_NONE

    def set_moves(self, moves):
        """
        Set the sequence of moves.

        Args:
            moves (str): The sequence of moves
        """
        self.moves = moves
        if self.moves:
            self.activate_driven(self.moves[-1])

    def activate_driven(self, symbol):
        """
        Activate driver by move symbol.

        Args:
            symbol (str): The move symbol

        Returns:
            bool: True if activated
        """
        for i, unit in enumerate(self.units):
            if unit.is_driven_by(symbol):
                self.set_active(i)
                self.switch = True
                return True
        return False

    def add_unit(self, unit):
        """
        Add unit under control.

        Args:
            unit: The unit to add
        """
        self.units.append(unit)

        # Find the initially active unit
        for i, unit in enumerate(self.units):
            if unit.start_active():
                self.set_active(i)
                return

        if self.units:
            self.set_active(0)

    def get_active(self):
        """
        Returns active unit or None.

        Returns:
            The active unit or None
        """
        if not self.units or self.active_index >= len(self.units):
            return None
        return self.units[self.active_index]

    def set_active(self, active_index):
        """Change active unit without triggering a switch animation."""
        if active_index != self.active_index:
            self.speedup = 0
            self.active_index = active_index

    def use_switch(self):
        """Activate the currently selected fish after a switch."""
        active = self.get_active()
        if active and not active.will_move():
            self.check_active()
            active = self.get_active()

        result = False
        if self.switch and active:
            if self.locker:
                self.locker.ensure_phases(3)
            active.activate()
            result = True

        self.switch = False
        return result

    def use_stroke(self):
        """Use a gathered one-shot keyboard stroke."""
        if self.stroke_symbol == ControlSym.SYM_NONE:
            return False

        self.make_move(self.stroke_symbol)
        self.stroke_symbol = ControlSym.SYM_NONE
        return True

    def drive_unit(self, input_provider):
        """Let the active unit, then any unit, drive from held input."""
        moved = ControlSym.SYM_NONE
        active = self.get_active()
        if active:
            moved = active.drive_borrowed(input_provider, self.arrows)

        if moved == ControlSym.SYM_NONE:
            for i, unit in enumerate(self.units):
                moved = unit.drive(input_provider)
                if moved != ControlSym.SYM_NONE:
                    self.set_active(i)
                    break

        if moved != ControlSym.SYM_NONE:
            self.moves += moved

        return moved != ControlSym.SYM_NONE

    def switch_active(self):
        """
        Switch active unit.
        Activate next driveable unit.
        """
        if not self.units:
            return

        start_index = self.active_index

        while True:
            self.active_index = (self.active_index + 1) % len(self.units)
            if self.active_index == start_index or self.units[self.active_index].can_drive():
                break

        if start_index != self.active_index:
            self.speedup = 0
            self.switch = True

    def make_move(self, move):
        """
        Make this move.

        Args:
            move (str): The move to make

        Returns:
            bool: False for bad move
        """
        for i, unit in enumerate(self.units):
            if unit.drive_order(move) == move:
                self.set_active(i)
                self.moves += move
                return True
        return False

    def cannot_move(self):
        """
        Returns true when there is no unit which will be able to move.

        Returns:
            bool: True if no unit can move
        """
        for unit in self.units:
            if unit.will_move():
                return False
        return True

    def lock_phases(self):
        """Ensure animation phases in the locker."""
        active = self.get_active()
        if active and active.is_moving():
            if active.is_pushing():
                self.speedup = 0
            elif not active.is_turning():
                self.speedup += 1

            if self.locker:
                self.locker.ensure_phases(self.get_needed_phases(self.speedup))
        else:
            self.speedup = 0

    def get_needed_phases(self, speedup):
        """Return animation phase count for the current movement speed."""
        speed_warp1 = 6
        speed_warp2 = 10

        active = self.get_active()
        if active is None:
            return 3
        if active.is_turning():
            return active.count_anim_phases("turn")
        if speedup > speed_warp2:
            return active.count_anim_phases("swam") // 6
        if speedup > speed_warp1:
            return active.count_anim_phases("swam") // 3
        return active.count_anim_phases("swam") // 2

    def check_active(self):
        """Check whether the active unit can still drive."""
        if not self.units:
            self.active_index = 0
        elif self.active_index >= len(self.units) or not self.units[self.active_index].can_drive():
            self.switch_active()

    def control_event(self, keystroke):
        """
        Handle keyboard event.

        Args:
            keystroke: The key stroke
        """
        if self.stroke_symbol != ControlSym.SYM_NONE:
            return

        key = keystroke.get_key()
        active = self.get_active()
        if active:
            self.stroke_symbol = active.my_symbol_borrowed(key, self.arrows)

        if self.stroke_symbol == ControlSym.SYM_NONE:
            for unit in self.units:
                self.stroke_symbol = unit.my_symbol(key)
                if self.stroke_symbol != ControlSym.SYM_NONE:
                    return

    def activate_selected(self, model):
        """
        Activate unit by model.

        Args:
            model: The model to activate

        Returns:
            bool: True if activated
        """
        for i, unit in enumerate(self.units):
            if unit.equals_model(model):
                self.set_active(i)
                self.switch = True
                return True
        return False

    def driving(self, input_provider):
        """
        Try to drive active unit.

        Args:
            input_provider: The input provider

        Returns:
            bool: True if driven
        """
        if self.use_switch():
            return False
        if self.use_stroke():
            return True
        return self.drive_unit(input_provider)

    # StepCounter interface implementation
    def get_step_count(self):
        """
        Get the total number of steps taken.

        Returns:
            int: The number of steps
        """
        return len(self.moves)

    def get_moves(self):
        """
        Get the sequence of moves taken.

        Returns:
            str: String representation of moves
        """
        return self.moves

    def is_powerful(self):
        """
        Returns true when active fish is powerful.

        Returns:
            bool: True if active fish is powerful
        """
        active = self.get_active()
        return active.is_powerful() if active else False

    def is_dangerous_move(self):
        """
        Returns true when the active fish is doing a dangerous move.

        Returns:
            bool: True if the move is dangerous
        """
        active = self.get_active()
        return active.is_pushing() if active else False
