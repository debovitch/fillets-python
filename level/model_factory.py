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
from gengine.v2 import V2
from level.cube import Cube
from level.control_sym import ControlSym
from level.dir import Dir
from level.key_control import KeyControl
from level.unit import Unit
from level.shape import Shape
from gengine.ex_info import ExInfo
from gengine.exceptions import LogicException

class ModelFactory:
    """
    Factory for creating game models (cubes, units, etc.).
    """
    
    @staticmethod
    def create_model(kind, loc, shape_str):
        """
        Add model at scene.
        
        Args:
            kind (str): Kind of item (e.g. "fish_big", "item_light", ...)
            loc (V2): Placement location
            shape_str (str): Shape definition string
        
        Returns:
            Cube: The created model
            
        Raises:
            LogicException: For unknown kind
        """
        if kind.startswith("output_"):
            return ModelFactory.create_output_item(kind, loc, shape_str)
        
        weight, power, alive = ModelFactory.create_params(kind)
        
        # Create a proper Shape object
        shape = Shape(shape_str)
        model = Cube(loc, weight, power, alive, shape)
        
        return model
    
    @staticmethod
    def create_params(kind):
        """
        Determine object parameters based on kind.
        
        Args:
            kind (str): Kind of item
            
        Returns:
            tuple: (weight, power, alive) parameters
            
        Raises:
            LogicException: When kind is unknown
        """
        if kind == "fish_small":
            return Cube.Weight.LIGHT, Cube.Weight.LIGHT, True
        elif kind == "fish_big":
            return Cube.Weight.LIGHT, Cube.Weight.HEAVY, True
        elif kind.startswith("fish_extra"):
            return Cube.Weight.LIGHT, Cube.Weight.LIGHT, True
        elif kind.startswith("fish_EXTRA"):
            return Cube.Weight.LIGHT, Cube.Weight.HEAVY, True
        else:
            power = Cube.Weight.NONE
            alive = False
            
            if kind == "item_light":
                weight = Cube.Weight.LIGHT
            elif kind == "item_heavy":
                weight = Cube.Weight.HEAVY
            elif kind == "item_fixed":
                weight = Cube.Weight.FIXED
            else:
                raise LogicException(ExInfo("unknown model kind")
                                    .add_info("kind", kind))
                
            return weight, power, alive
    
    @staticmethod
    def create_unit(kind):
        """
        Create unit for driveable fish.
        
        Args:
            kind (str): Kind of item (e.g. "fish_big", "fish_small", ...)
            
        Returns:
            Unit: New unit or None
        """
        result = None
        
        if kind == "fish_small":
            smallfish = KeyControl()
            smallfish.set_up(pygame.K_i)
            smallfish.set_down(pygame.K_k)
            smallfish.set_left(pygame.K_j)
            smallfish.set_right(pygame.K_l)
            result = Unit(smallfish, ControlSym('u', 'd', 'l', 'r'), True)
        elif kind == "fish_big":
            bigfish = KeyControl()
            bigfish.set_up(pygame.K_w)
            bigfish.set_down(pygame.K_s)
            bigfish.set_left(pygame.K_a)
            bigfish.set_right(pygame.K_d)
            result = Unit(bigfish, ControlSym('U', 'D', 'L', 'R'))
        elif kind.startswith("fish_extra") or kind.startswith("fish_EXTRA"):
            extrafish = KeyControl()
            # Using a placeholder for unassigned keys
            extrafish.set_up(pygame.K_UNKNOWN if hasattr(pygame, 'K_UNKNOWN') else 0)
            extrafish.set_down(pygame.K_UNKNOWN if hasattr(pygame, 'K_UNKNOWN') else 0)
            extrafish.set_left(pygame.K_UNKNOWN if hasattr(pygame, 'K_UNKNOWN') else 0)
            extrafish.set_right(pygame.K_UNKNOWN if hasattr(pygame, 'K_UNKNOWN') else 0)
            result = Unit(extrafish, ModelFactory.parse_extra_control_sym(kind))
            
        return result
    
    @staticmethod
    def create_border():
        """
        Create special model for outer space (border around the field).
        
        Returns:
            Cube: Border cube
        """
        border_shape = Shape("X\n")
        border = Cube(V2(-1, -1), Cube.Weight.FIXED, Cube.Weight.NONE, False, border_shape)
        return border
    
    @staticmethod
    def create_output_item(kind, loc, shape_str):
        """
        Create a one-way output out of room.
        
        Args:
            kind (str): Direction of output ("output_left", etc.)
            loc (V2): Location of the output
            shape_str (str): Shape definition string
            
        Returns:
            Cube: Output cube
            
        Raises:
            LogicException: When output direction is unknown
        """
        out_dir = Dir.DIR_NO
        
        if kind == "output_left":
            out_dir = Dir.DIR_LEFT
        elif kind == "output_right":
            out_dir = Dir.DIR_RIGHT
        elif kind == "output_up":
            out_dir = Dir.DIR_UP
        elif kind == "output_down":
            out_dir = Dir.DIR_DOWN
        else:
            raise LogicException(ExInfo("unknown border dir")
                                .add_info("kind", kind))
        
        shape = Shape(shape_str)
        model = Cube(loc, Cube.Weight.FIXED, Cube.Weight.NONE, False, shape)
        model.set_out_dir(out_dir)
        return model
    
    @staticmethod
    def parse_extra_control_sym(kind):
        """
        Define control symbols for extra fish.
        Format: "fish_extra-UDLR"
        
        Args:
            kind (str): Kind specification with control symbols
            
        Returns:
            ControlSym: Parsed control symbols
            
        Raises:
            LogicException: When symbols aren't specified correctly
        """
        prefix = "fish_extra-"
        prefix_upper = "fish_EXTRA-"
        
        if kind.startswith(prefix) and len(kind) == len(prefix) + 4:
            offset = len(prefix)
        elif kind.startswith(prefix_upper) and len(kind) == len(prefix_upper) + 4:
            offset = len(prefix_upper)
        else:
            raise LogicException(ExInfo("you must specify control symbols")
                               .add_info("kind", kind))
        
        up = kind[offset]
        down = kind[offset + 1]
        left = kind[offset + 2]
        right = kind[offset + 3]
        
        return ControlSym(up, down, left, right)