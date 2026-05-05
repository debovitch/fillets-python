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
from typing import Dict, Optional, Union
from enum import Enum

from gengine.v2 import V2
from gengine.path import Path
from gengine.resource.res_image_pack import ResImagePack
from gengine.log import log_warning
from gengine.ex_info import ExInfo

from effect.view_effect import ViewEffect
from effect.effect_none import EffectNone
from effect.effect_mirror import EffectMirror
from effect.effect_invisible import EffectInvisible
from effect.effect_reverse import EffectReverse
from effect.effect_zx import EffectZx

class Side(str, Enum):
    """Enum representing animation sides"""
    LEFT = "left"
    RIGHT = "right"

def _to_side(side):
    if side == 0:
        return Side.LEFT
    if side == 1:
        return Side.RIGHT
    return Side(side) if isinstance(side, str) else side

class Anim:
    """
    Animation sprite.
    Handles animation frames, effects, and drawing.
    """
    
    def __init__(self):
        """Create new animation sprite."""
        self._effect = EffectNone()
        self._view_shift = V2(0, 0)
        self._anim_pack = {
            Side.LEFT: ResImagePack(),
            Side.RIGHT: ResImagePack()
        }
        
        self._anim_name = ""
        self._anim_phase = 0
        self._run = False
        self._special_anim_name = ""
        self._special_anim_phase = 0
        self._used_path = ""

    def __del__(self):
        """Release animation image packs."""
        self.clean()

    def clean(self):
        """Release resources held by this animation."""
        if getattr(self, "_anim_pack", None):
            for pack in self._anim_pack.values():
                if pack:
                    pack.remove_all()
            self._anim_pack = {}
        self._effect = None
    
    def draw_at(self, screen: pygame.Surface, x: int, y: int, side: str):
        """
        Draw anim phase at screen position.
        Increase phase when anim is running.
        
        Args:
            screen: The screen to draw on
            x: X coordinate
            y: Y coordinate
            side: Which side to draw ('left' or 'right')
        """
        # Convert string to Side enum if needed
        side_enum = _to_side(side)
        
        if not self._effect.is_invisible():
            # Draw main animation
            if self._anim_name and self._anim_pack[side_enum].count_res(self._anim_name) > 0:
                surface = self._anim_pack[side_enum].get_res(self._anim_name, self._anim_phase)
                if surface:
                    self._effect.blit(screen, surface, x, y)
                
                # Update animation phase if running
                if self._run:
                    self._anim_phase += 1
                    if self._anim_phase >= self._anim_pack[side_enum].count_res(self._anim_name):
                        self._anim_phase = 0
            
            # Draw special animation if present
            if self._special_anim_name and self._anim_pack[side_enum].count_res(self._special_anim_name) > 0:
                surface = self._anim_pack[side_enum].get_res(self._special_anim_name, self._special_anim_phase)
                if surface:
                    self._effect.blit(screen, surface, x, y)
        
        # Update effect
        self._effect.update_effect()
    
    def add_anim(self, name: str, picture, side=Side.LEFT):
        """
        Add picture to anim.
        
        Args:
            name: Animation name
            picture: Picture path or pygame Surface
            side: Which side to add (Side.LEFT or Side.RIGHT)
        """
        # Convert string to Side enum if needed
        side_enum = _to_side(side)
        
        if isinstance(picture, Path):
            self._used_path = picture.get_native()
            self._anim_pack[side_enum].add_image(name, picture)
        else:
            # Assume it's a pygame Surface
            self._anim_pack[side_enum].add_res(name, picture)
    
    def run_anim(self, name: str, start_phase: int = 0):
        """
        Run this animation.
        
        Args:
            name: Animation name
            start_phase: Starting phase
        """
        if self._anim_name != name:
            self.set_anim(name, start_phase)
        self._run = True
    
    def set_anim(self, name: str, phase: int):
        """
        Set static visage.
        
        Args:
            name: Animation name
            phase: Animation phase
        """
        self._run = False
        self._anim_name = name
        self._anim_phase = phase
        
        count = self._anim_pack[Side.LEFT].count_res(name)
        if self._anim_phase >= count:
            if count == 0:
                self._anim_phase = 0
            else:
                self._anim_phase %= count
            
            log_warning(ExInfo("anim phase over-flow")
                       .add_info("anim", name)
                       .add_info("phase", phase)
                       .add_info("count", count)
                       .add_info("usedPath", self._used_path))
    
    def use_special_anim(self, name: str, phase: int):
        """
        Use special effect for one phase.
        Effect will be blited in second layer.
        
        Args:
            name: Anim name, empty is no anim
            phase: Anim phase
        """
        self._special_anim_name = name
        self._special_anim_phase = phase
        
        if not self._special_anim_name:
            return
        
        count = self._anim_pack[Side.LEFT].count_res(name)
        if self._special_anim_phase >= count:
            if count == 0:
                self._special_anim_name = ""
                self._special_anim_phase = 0
            else:
                self._special_anim_phase %= count
            
            log_warning(ExInfo("special anim phase over-flow")
                       .add_info("anim", name)
                       .add_info("phase", phase)
                       .add_info("count", count))
    
    def change_effect(self, new_effect: ViewEffect):
        """
        Change effect.
        
        Args:
            new_effect: New effect to use
            
        Raises:
            ValueError: If new_effect is None
        """
        if new_effect is None:
            raise ValueError(ExInfo("new_effect is None")
                           .add_info("animName", self._anim_name)
                           .add_info("specialAnimName", self._special_anim_name))
        
        self._effect = new_effect
    
    def is_disintegrated(self) -> bool:
        """
        Check if the animation is disintegrated.
        
        Returns:
            True if disintegrated, False otherwise
        """
        return self._effect.is_disintegrated()
    
    def is_invisible(self) -> bool:
        """
        Check if the animation is invisible.
        
        Returns:
            True if invisible, False otherwise
        """
        return self._effect.is_invisible()
    
    def set_view_shift(self, shift: V2):
        """
        Set the view shift.
        
        Args:
            shift: New view shift
        """
        self._view_shift = shift
    
    def get_view_shift(self) -> V2:
        """
        Get the view shift.
        
        Returns:
            Current view shift
        """
        return self._view_shift
    
    def set_effect(self, effect_name: str):
        """
        Set effect by name.
        
        Args:
            effect_name: Name of the effect
        """
        if effect_name == EffectNone.NAME:
            self.change_effect(EffectNone())
        elif effect_name == EffectMirror.NAME:
            self.change_effect(EffectMirror())
        elif effect_name == EffectInvisible.NAME:
            self.change_effect(EffectInvisible())
        elif effect_name == EffectReverse.NAME:
            self.change_effect(EffectReverse())
        elif effect_name == EffectZx.NAME:
            self.change_effect(EffectZx())
        else:
            log_warning(ExInfo("unknown view effect")
                       .add_info("effect", effect_name))
    
    def count_anim_phases(self, anim: str, side=Side.LEFT) -> int:
        """
        Count animation phases.
        
        Args:
            anim: Animation name
            side: Which side to count
            
        Returns:
            Number of phases
        """
        # Convert string to Side enum if needed
        side_enum = Side(side) if isinstance(side, str) else side
        return self._anim_pack[side_enum].count_res(anim)
    
    @staticmethod
    def _encode(value):
        """Encode a value for state serialization."""
        if isinstance(value, str):
            output = value
            output = output.replace("&", "&amp;")
            output = output.replace(",", "&comma;")
            return output
        elif isinstance(value, bool):
            return "1" if value else "0"
        else:
            return str(value)
    
    @staticmethod
    def _decode(value: str) -> str:
        """Decode a value from state serialization."""
        output = value
        output = output.replace("&comma;", ",")
        output = output.replace("&amp;", "&")
        return output
    
    @staticmethod
    def _decode_int(value: str) -> int:
        """Decode an integer from state serialization."""
        try:
            return int(value)
        except ValueError:
            log_warning(ExInfo("invalid int")
                       .add_info("input", value))
            return 0
    
    def get_state(self) -> str:
        """
        Get serialized state.
        
        Returns:
            Serialized state string
        """
        output = []
        output.append(self._encode(self._effect.get_name()))
        output.append(self._encode(self._view_shift.get_x()))
        output.append(self._encode(self._view_shift.get_y()))
        output.append(self._encode(self._anim_name))
        output.append(self._encode(self._anim_phase))
        output.append(self._encode(self._run))
        output.append(self._encode(self._special_anim_name))
        output.append(self._encode(self._special_anim_phase))
        
        return ",".join(output)
    
    def restore_state(self, state: str):
        """
        Restore from serialized state.
        
        Args:
            state: Serialized state string
        """
        values = state.split(',')
        if len(values) != 8:
            log_warning(ExInfo("invalid anim state")
                       .add_info("state", state))
            return
        
        i = 0
        effect_name = self._decode(values[i]); i += 1
        x = self._decode_int(values[i]); i += 1
        y = self._decode_int(values[i]); i += 1
        self._anim_name = self._decode(values[i]); i += 1
        self._anim_phase = self._decode_int(values[i]); i += 1
        self._run = bool(self._decode_int(values[i])); i += 1
        self._special_anim_name = self._decode(values[i]); i += 1
        self._special_anim_phase = self._decode_int(values[i]); i += 1
        
        self.set_effect(effect_name)
        self._view_shift = V2(x, y)
