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

from enum import Enum, auto
from gengine.no_copy import NoCopy
from gengine.v2 import V2
from level.dir import Dir
from level.goal import Goal

class Cube(NoCopy):
    """
    A game object with physical properties.
    The basic building block of the game world.
    """
    
    class Weight(Enum):
        """
        Weight/solidity of an object.
        """
        NONE = 0    # No weight, not solid
        LIGHT = 1   # Light object
        HEAVY = 2   # Heavy object
        FIXED = 3   # Fixed, immovable object
    
    class Action(Enum):
        """
        Current action state of an object.
        """
        ACTION_NO = 0     # No action
        ACTION_FALL = 1   # Falling
        ACTION_MOVE = 2   # Moving
    
    def __init__(self, location, weight, power, alive, shape=None):
        """
        Initialize a new cube.
        
        Args:
            location (V2): The location of the cube
            weight (Cube.Weight): The weight of the cube
            power (Cube.Weight): The pushing power of the cube
            alive (bool): Whether the cube is alive
            shape: The visual shape of the cube
        """
        self.index = -1  # No index assigned yet
        self.busy = False
        self.loc = location
        self.alive = alive
        self.out = False
        self.weight = weight
        self.power = power
        self.look_left = True  # Match C++ default
        self.lost = False
        
        self.shape = shape
        from level.anim import Anim
        self.anim = Anim()
        self.goal = Goal.no_goal()
        self.out_dir = Dir.DIR_NO
        self.out_capacity = 0
        self.dialogs = None
        
        # Create Rules instance for this cube if needed. Delay the import
        # to avoid circular imports.
        self.rules = None

    def __del__(self):
        """Release resources held by the cube."""
        self.clean()

    def clean(self):
        """Release owned resources."""
        if self.anim:
            self.anim.clean()
            self.anim = None
        self.rules = None
        self.shape = None
        self.dialogs = None
    
    def create_rules(self):
        """
        Create the rules instance for this cube if it doesn't exist yet.
        """
        if self.rules is None:
            from level.rules import Rules
            self.rules = Rules(self)
    
    def set_goal(self, goal):
        """
        Set the goal for this cube.
        
        Args:
            goal (Goal): The goal to set
        """
        self.goal = goal
    
    def set_index(self, model_index):
        """
        Set the index of this cube.
        
        Args:
            model_index (int): The index to set
        """
        self.index = model_index
    
    def get_index(self):
        """
        Get the index of this cube.
        
        Returns:
            int: The index of this cube
        """
        return self.index
    
    def is_busy(self):
        """
        Check if this cube is busy.
        
        Returns:
            bool: True if the cube is busy
        """
        return self.busy
    
    def set_busy(self, busy):
        """
        Set whether this cube is busy.
        
        Args:
            busy (bool): Whether the cube is busy
        """
        self.busy = busy
    
    def change_die(self):
        """
        Change the cube to be dead.
        """
        from effect.effect_disintegrate import EffectDisintegrate

        self.alive = False
        self.anim.change_effect(EffectDisintegrate())
    
    def change_going_out(self):
        """
        Make the object unmovable when it is going out of the room.
        """
        self.weight = Cube.Weight.FIXED
    
    def change_go_out(self):
        """
        Change the cube to be out.
        """
        self.out = True
        self.change_remove()
    
    def change_remove(self):
        """
        Remove the cube from the game.
        """
        self.lost = True
        self.weight = Cube.Weight.NONE
        # HACK: object is moved out, same as in C++ implementation
        self.loc = V2(-1000, -1000)
    
    def change_turn_side(self):
        """
        Change the cube to turn to the other side.
        """
        self.look_left = not self.look_left
    
    def change_set_location(self, loc):
        """
        Change the location of this cube.
        
        Args:
            loc (V2): The new location
        """
        self.loc = loc
    
    def get_location(self):
        """
        Get the location of this cube.
        
        Returns:
            V2: The location of this cube
        """
        return self.loc
    
    def is_alive(self):
        """
        Check if this cube is alive.
        
        Returns:
            bool: True if the cube is alive
        """
        return self.alive
    
    def is_left(self):
        """
        Check if this cube is looking left.
        
        Returns:
            bool: True if the cube is looking left
        """
        return self.look_left
    
    def is_out(self):
        """
        Check if this cube is out of the room.
        
        Returns:
            bool: True if the cube is out
        """
        return self.out
    
    def is_lost(self):
        """
        Check if this cube is lost.
        
        Returns:
            bool: True if the cube is lost
        """
        return self.lost
    
    def is_satisfy(self):
        """
        Check if this cube satisfies its goal.
        
        Returns:
            bool: True if the cube satisfies its goal
        """
        return self.goal.is_satisfy(self)
    
    def is_wrong(self):
        """
        Check if this cube's goal is wrong.
        
        Returns:
            bool: True if the cube's goal is wrong
        """
        return self.goal.is_wrong(self)
    
    def is_wall(self):
        """
        Check if this cube is a wall.
        
        Returns:
            bool: True if the cube is a wall
        """
        return self.weight.value >= Cube.Weight.FIXED.value
    
    def should_go_out(self):
        """
        Check if this cube should go out.
        
        Returns:
            bool: True if the cube should go out
        """
        return self.goal.should_go_out()
    
    def is_border(self):
        """
        Check if this cube is a border.
        
        Returns:
            bool: True if the cube is a border
        """
        return self.index == -1
    
    def get_weight(self):
        """
        Get the weight of this cube.
        
        Returns:
            Cube.Weight: The weight of this cube
        """
        return self.weight
    
    def get_power(self):
        """
        Get the power of this cube.
        
        Returns:
            Cube.Weight: The power of this cube
        """
        return self.power
    
    def get_shape(self):
        """
        Get the shape of this cube.
        
        Returns:
            The shape of this cube
        """
        return self.shape
    
    def get_last_move_dir(self):
        """
        Get the last movement direction of this cube.
        
        Returns:
            Dir: The last movement direction
        """
        if self.rules:
            return self.rules.get_dir()
        return Dir.DIR_NO
    
    def is_out_dir(self, dir):
        """
        Check if this cube can go out in the given direction.
        
        Args:
            dir (Dir): The direction to check
            
        Returns:
            bool: True if the cube can go out in the given direction
        """
        return self.out_dir == dir
    
    def get_out_dir(self):
        """
        Get the direction in which this cube can go out.
        
        Returns:
            Dir: The direction in which this cube can go out
        """
        return self.out_dir
    
    def get_out_capacity(self):
        """
        Get the capacity of the out direction.
        
        Returns:
            int: The capacity of the out direction
        """
        return self.out_capacity
    
    def set_out_dir(self, out_dir, capacity=2, weight=Weight.FIXED):
        """
        Set the direction in which this cube can go out.
        
        Args:
            out_dir (Dir): The direction in which this cube can go out
            capacity (int): The capacity of the out direction
            weight (Cube.Weight): The weight of the out direction
        """
        self.out_capacity = capacity
        self.out_dir = out_dir
        self.weight = weight
    
    def dec_out_capacity(self):
        """
        Decrease the capacity of the out direction.
        Special model 'output_DIR' has capacity to absorb fishes,
        then it changes to normal 'item_light'.
        """
        if self.out_capacity > 0:
            self.out_capacity -= 1
            if self.out_capacity == 0:
                self.out_dir = Dir.DIR_NO
                self.weight = Cube.Weight.LIGHT
                self.out_capacity = -1
    
    def set_extra_params(self):
        """
        Set extra parameters from a saved undo state.
        They restore just the parameters used by the View.
        """
        self.lost = False
        if self.rules:
            self.rules.reset_last_dir()
    
    def is_talking(self):
        """
        Check if this cube is talking.
        
        Returns:
            bool: True if the cube is talking
        """
        return self.dialogs and hasattr(self.dialogs, 'is_talking') and self.dialogs.is_talking(self.index)
    
    def take_dialogs(self, dialogs):
        """
        Set the dialogs for this cube.
        
        Args:
            dialogs: The dialogs to set
        """
        self.dialogs = dialogs
    
    def is_disintegrated(self):
        """
        Check if this cube is disintegrated.
        
        Returns:
            bool: True if the cube is disintegrated
        """
        return self.anim and hasattr(self.anim, 'is_disintegrated') and self.anim.is_disintegrated()
    
    def is_invisible(self):
        """
        Check if this cube is invisible.
        
        Returns:
            bool: True if the cube is invisible
        """
        return self.anim and hasattr(self.anim, 'is_invisible') and self.anim.is_invisible()
    
    def anim(self):
        """
        Get the animation of this cube.
        
        Returns:
            The animation of this cube
        """
        return self.anim
    
    def get_rules(self):
        """
        Get the rules of this cube.
        
        Returns:
            The rules of this cube
        """
        if not self.rules:
            self.create_rules()
        return self.rules
    
    def to_string(self):
        """
        Get a string representation of this cube.
        
        Returns:
            str: A string representation of this cube
        """
        info = {
            "loc": str(self.loc),
            "alive": str(self.alive),
            "weight": str(self.weight),
            "power": str(self.power)
        }
        if self.shape:
            info["shape"] = str(self.shape)
        
        return f"Cube[{', '.join([f'{k}={v}' for k, v in info.items()])}]"
    
    def __str__(self):
        """
        Get a string representation of this cube.
        
        Returns:
            str: A string representation of this cube
        """
        return self.to_string()
