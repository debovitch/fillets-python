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
from level.dir import Dir
from level.cube import Cube
from level.mark_mask import MarkMask
from gengine.ex_info import ExInfo
from level.layout_exception import LayoutException


def _weight_value(weight):
    return weight.value if hasattr(weight, "value") else weight


class Rules(NoCopy):
    """
    Game rules implementation for objects in the field.
    Handles movement, physics, and game logic.
    """
    
    def __init__(self, model):
        """
        Create new rules for model.
        
        Args:
            model (Cube): The model this rules object controls
        """
        self.m_ready_to_die = False
        self.m_ready_to_turn = False
        self.m_ready_to_active = False
        self.m_dir = Dir.DIR_NO
        self.m_pushing = False
        self.m_out_depth = 0
        self.m_touch_dir = Dir.DIR_NO
        
        self.m_model = model
        self.m_mask = None
        self.m_last_fall = False
    
    def __del__(self):
        """
        Clean up resources when the rules are deleted.
        """
        if self.m_mask:
            self.m_mask.unmask()
            self.m_mask = None
    
    def take_field(self, field):
        """
        Connect model with field.
        
        Args:
            field (Field): The field to connect to
            
        Raises:
            LayoutException: If the location is already occupied
        """
        if self.m_mask:
            self.m_mask.unmask()
            self.m_mask = None
        
        self.m_mask = MarkMask(self.m_model, field)
        resist = self.m_mask.get_resist(Dir.DIR_NO)
        if resist:
            raise LayoutException(ExInfo("position is occupied")
                                 .add_info("model", str(self.m_model))
                                 .add_info("resist", str(resist[0])))
        
        self.m_mask.mask()
    
    def occupy_new_pos(self):
        """
        Accomplish last move in m_dir direction.
        Mask to a new position.
        Change model position.
        """
        self.m_touch_dir = Dir.DIR_NO
        if self.m_dir != Dir.DIR_NO:
            self.m_pushing = False
            
            shift = Dir.dir2xy(self.m_dir)
            old_loc = self.m_model.get_location()
            self.m_model.change_set_location(old_loc.plus(shift))
            
            self.m_mask.mask()
    
    def change_set_location(self, loc):
        """
        Force model to a new position.
        Used just for undo loading.
        
        Args:
            loc (V2): The new location
        """
        self.m_mask.unmask()
        # HACK: model.out flag is recognized by its location
        if loc.get_x() < 0 and loc.get_y() < 0:
            self.m_model.change_go_out()
        else:
            self.m_model.change_set_location(loc)
            self.m_mask.mask()
    
    def check_dead(self, last_action):
        """
        Check if fish has died.
        
        Args:
            last_action (Cube.Action): The last action performed
            
        Returns:
            bool: True if the fish has died
        """
        dead = False
        
        if self.m_model.is_alive():
            if last_action == Cube.Action.ACTION_FALL:
                dead = self.check_dead_fall()
            elif last_action == Cube.Action.ACTION_MOVE:
                dead = self.check_dead_move()
            
            if not dead:
                dead = self.check_dead_stress()
            
            if dead:
                self.m_ready_to_die = True
        
        return dead
    
    def check_dead_move(self):
        """
        Check if fish has died due to movement.
        
        Returns:
            bool: True if the fish has died
        """
        from gengine.agent.option_agent import OptionAgent
        
        strict = OptionAgent.agent().get_as_bool("strict_rules", True)
        
        resist = self.m_mask.get_resist(Dir.DIR_UP)
        for model in resist:
            if not model.is_alive():
                resist_dir = model.get_rules().get_dir()
                if resist_dir != Dir.DIR_NO and resist_dir != Dir.DIR_UP:
                    if strict:
                        if model.get_rules().is_on_holder_backs():
                            return True
                    else:
                        if not model.get_rules().is_on_stack():
                            return True
        
        return False
    
    def check_dead_fall(self):
        """
        Check if fish has died due to falling.
        
        Returns:
            bool: True if the fish has died
        """
        killers = self.who_is_falling()
        
        for model in killers:
            if not model.get_rules().is_on_wall():
                return True
        
        return False
    
    def check_dead_stress(self):
        """
        Check if fish has died due to stress.
        
        Returns:
            bool: True if the fish has died
        """
        killers = self.who_is_heavier(self.m_model.get_power())
        
        for model in killers:
            if not model.get_rules().is_on_strong_pad(model.get_weight()):
                return True
        
        return False
    
    def change_state(self):
        """
        Finish events from last round.
        Change model state.
        """
        self.m_dir = Dir.DIR_NO
        
        if not self.m_model.is_lost() and self.m_model.is_disintegrated():
            self.m_mask.unmask()
            self.m_model.change_remove()
        
        if self.m_ready_to_turn:
            self.m_ready_to_turn = False
            self.m_model.change_turn_side()
        
        self.m_ready_to_active = False
        
        if self.m_ready_to_die:
            self.m_ready_to_die = False
            self.m_model.change_die()
    
    def action_out(self):
        """
        Let model go out of room.
        
        Returns:
            int: out depth, 0 for normal, 1 for going out,
                 2+ for on the way, -1 for out of screen
        """
        if (not self.m_model.is_lost() and 
            not self.m_model.is_busy() and 
            self.m_dir == Dir.DIR_NO):
            
            if self.m_model.should_go_out():
                if self.m_mask.is_fully_out():
                    self.m_model.change_go_out()
                    self.m_out_depth = -1
                else:
                    border_dir = self.m_mask.get_border_dir()
                    if border_dir != Dir.DIR_NO:
                        self.m_model.change_going_out()
                        self.move_dir_brute(border_dir)
                        self.m_out_depth += 1
                    else:
                        self.m_out_depth = 0
        
        return self.m_out_depth
    
    def action_fall(self):
        """
        Let model fall.
        """
        self.m_dir = Dir.DIR_DOWN
        self.m_last_fall = True
    
    def clear_last_fall(self):
        """
        Unset falling flag.
        
        Returns:
            bool: last value of the flag
        """
        last = self.m_last_fall
        self.m_last_fall = False
        return last
    
    def free_old_pos(self):
        """
        Unmask from old position.
        """
        if self.m_dir != Dir.DIR_NO:
            self.m_mask.unmask()
    
    def is_on_cond(self, cond):
        """
        Whether object is direct or indirect on something specific.
        
        Args:
            cond (OnCondition): condition which will be satisfied when object is on.
            
        Returns:
            bool: True if the condition is satisfied
        """
        result = False
        if cond.is_satisfy(self.m_model):
            result = True
        elif cond.is_wrong(self.m_model):
            result = False
        else:
            self.m_mask.unmask()
            
            resist = self.m_mask.get_resist(Dir.DIR_DOWN)
            for model in resist:
                if model.get_rules().is_on_cond(cond):
                    result = True
                    break
            
            self.m_mask.mask()
        
        return result
    
    def is_on_stack(self):
        """
        Whether object is on another unlive object that is on something fixed.
        
        Returns:
            bool: True if the object is on a stack
        """
        from level.on_stack import OnStack
        return self.is_on_cond(OnStack())
    
    def is_on_wall(self):
        """
        Whether object is direct or indirect on a wall.
        
        Returns:
            bool: True if the object is on a wall
        """
        from level.on_wall import OnWall
        return self.is_on_cond(OnWall())
    
    def is_on_strong_pad(self, weight):
        """
        Whether object is direct or indirect on Wall or on powerful fish.
        
        Args:
            weight (Cube.Weight): stress weight which must fish carry
            
        Returns:
            bool: True if Wall or a strong fish carry this object
        """
        from level.on_strong_pad import OnStrongPad
        return self.is_on_cond(OnStrongPad(weight))
    
    def is_on_holder_backs(self):
        """
        Returns true if the object is laying just on alive holders
        and they all have at least a part of their backs directly under this object.
        
        Returns:
            bool: True if the object is on holder backs
        """
        num_direct_holders = 0
        resist = self.m_mask.get_resist(Dir.DIR_DOWN)
        for model in resist:
            if model.is_alive():
                num_direct_holders += 1
        
        pads = self.get_pads()
        from level.mark_mask import MarkMask
        MarkMask.unique(pads)
        return num_direct_holders == len(pads)
    
    def get_pads(self):
        """
        Returns all alive fish and walls under this object.
        
        Returns:
            list: List of models under this object
        """
        pads = []
        self.m_mask.unmask()
        
        resist = self.m_mask.get_resist(Dir.DIR_DOWN)
        for model in resist:
            if model.is_alive() or model.is_wall():
                pads.append(model)
            else:
                distance_pads = model.get_rules().get_pads()
                pads.extend(distance_pads)
        
        self.m_mask.mask()
        return pads
    
    def is_falling(self):
        """
        Whether object is falling.
        
        Returns:
            bool: True if the object is falling
        """
        result = False
        if not self.m_model.is_alive():
            result = (self.m_dir == Dir.DIR_DOWN)
        return result
    
    def who_is_falling(self):
        """
        Who is falling on us.
        
        Returns:
            list: Array of killers, they can fall indirect on us
        """
        result = []
        self.m_mask.unmask()
        
        resist = self.m_mask.get_resist(Dir.DIR_UP)
        for model in resist:
            # NOTE: falling is not propagated over fish
            if not model.is_wall() and not model.is_alive():
                if model.get_rules().is_falling():
                    result.append(model)
                else:
                    distance_killers = model.get_rules().who_is_falling()
                    result.extend(distance_killers)
        
        self.m_mask.mask()
        return result
    
    def is_heavier(self, power):
        """
        Whether object is heavier than our power.
        
        Args:
            power (Cube.Weight): our max power
            
        Returns:
            bool: True if the object is heavier
        """
        result = False
        if not self.m_model.is_wall() and not self.m_model.is_alive():
            if _weight_value(self.m_model.get_weight()) > _weight_value(power):
                result = True
        
        return result
    
    def who_is_heavier(self, power):
        """
        Who is heavier than our power.
        
        Args:
            power (Cube.Weight): our max power
            
        Returns:
            list: Array of killers, they can lie indirect on us
        """
        result = []
        self.m_mask.unmask()
        
        resist = self.m_mask.get_resist(Dir.DIR_UP)
        for model in resist:
            if not model.is_wall():
                if model.get_rules().is_heavier(power):
                    result.append(model)
                else:
                    distance_killers = model.get_rules().who_is_heavier(power)
                    result.extend(distance_killers)
        
        self.m_mask.mask()
        return result
    
    def can_move_others(self, dir, power):
        """
        Whether other will retreat before us.
        
        Args:
            dir (Dir): The direction to move
            power (Cube.Weight): we will use this power
            
        Returns:
            bool: True if we can move others
        """
        result = True
        self.m_mask.unmask()
        
        resist = self.m_mask.get_resist(dir)
        for model in resist:
            if self.m_model.should_go_out() and model.is_border():
                continue
            if not model.get_rules().can_dir(dir, power):
                result = False
                break
        
        self.m_mask.mask()
        return result
    
    def can_dir(self, dir, power):
        """
        Whether others can move us.
        
        Args:
            dir (Dir): move direction
            power (Cube.Weight): others power
            
        Returns:
            bool: True if we can move
        """
        result = False
        if (not self.m_model.is_alive()
                and _weight_value(power) >= _weight_value(self.m_model.get_weight())):
            # A special case when outgoing object is pushing with FIXED power.
            if self.m_model.is_wall() and not self.m_model.should_go_out():
                return False
            result = self.can_move_others(dir, power)
        
        return result
    
    def touch_spec(self, dir):
        """
        There is one special case.
        When model touches output_DIR then it goes out.
        
        Args:
            dir (Dir): The direction to touch
            
        Returns:
            bool: True if the model went out
        """
        result = False
        resist = self.m_mask.get_resist(dir)
        if len(resist) == 1:
            if resist[0].is_out_dir(dir):
                resist[0].dec_out_capacity()
                self.m_mask.unmask()
                self.m_model.change_go_out()
                result = True
        return result
    
    def set_touched(self, dir):
        """
        Marks all resisted models as touched.
        
        Args:
            dir (Dir): The direction to touch
        """
        self.m_touch_dir = dir
        if not self.m_model.is_wall():
            self.m_mask.unmask()
            resist = self.m_mask.get_resist(dir)
            for model in resist:
                if not model.is_alive():
                    model.get_rules().set_touched(dir)
            self.m_mask.mask()
    
    def action_move_dir(self, dir):
        """
        Try to move.
        Only m_dir will be set.
        
        Args:
            dir (Dir): The direction to move
            
        Returns:
            bool: True if we have moved
        """
        result = False
        if self.can_move_others(dir, self.m_model.get_power()):
            self.move_dir_brute(dir)
            result = True
        else:
            if self.touch_spec(dir):
                result = True
            else:
                self.set_touched(dir)
        
        return result
    
    def move_dir_brute(self, dir):
        """
        Irrespective move.
        Set m_dir to this dir and do the same for all resist.
        
        Args:
            dir (Dir): The direction to move
        """
        self.m_mask.unmask()
        
        resist = self.m_mask.get_resist(dir)
        for model in resist:
            if not model.is_border():
                model.get_rules().move_dir_brute(dir)
                self.m_pushing = True
        
        self.m_dir = dir
        self.m_mask.mask()
    
    def get_action(self):
        """
        Return what we do the last round.
        
        Returns:
            str: The last action
        """
        if self.m_ready_to_turn:
            return "turn"
        elif self.m_ready_to_active:
            return "activate"
        elif self.m_model.is_busy():
            return "busy"
        
        if self.m_dir == Dir.DIR_LEFT:
            return "move_left"
        elif self.m_dir == Dir.DIR_RIGHT:
            return "move_right"
        elif self.m_dir == Dir.DIR_UP:
            return "move_up"
        elif self.m_dir == Dir.DIR_DOWN:
            return "move_down"
        elif self.m_dir == Dir.DIR_NO:
            return "rest"
        else:
            assert False, "unknown dir"
        
        return "rest"
    
    def get_state(self):
        """
        Return how we have feel the last round.
        
        Returns:
            str: The last state
        """
        if self.m_out_depth == 1:
            return "goout"
        elif not self.m_model.is_alive():
            return "dead"
        elif self.m_model.is_talking():
            return "talking"
        elif self.m_pushing:
            return "pushing"
        else:
            return "normal"
    
    def is_at_border(self):
        """
        Check if the model is at a border.
        
        Returns:
            bool: True if the model is at a border
        """
        return self.m_mask.get_border_dir() != Dir.DIR_NO
    
    def is_free_place(self, loc):
        """
        Check if a location is free.
        
        Args:
            loc (V2): The location to check
            
        Returns:
            bool: True if the location is free
        """
        return not self.m_mask.get_placed_resist(loc)
    
    def get_resist(self, dir):
        """
        Get the models resisting in a direction.
        
        Args:
            dir (Dir): The direction to check
            
        Returns:
            list: The models resisting in that direction
        """
        return self.m_mask.get_resist(dir)
    
    def get_dir(self):
        """
        Get the current direction.
        
        Returns:
            Dir: The current direction
        """
        return self.m_dir
    
    def get_touch_dir(self):
        """
        Get the touch direction.
        
        Returns:
            Dir: The touch direction
        """
        return self.m_touch_dir
    
    def is_pushing(self):
        """
        Check if the model is pushing.
        
        Returns:
            bool: True if the model is pushing
        """
        return self.m_pushing
    
    def reset_last_dir(self):
        """
        Reset the last direction.
        """
        self.m_dir = Dir.DIR_NO
    
    def action_turn_side(self):
        """
        Turn the model to the other side.
        """
        self.m_ready_to_turn = True
    
    def action_activate(self):
        """
        Activate the model.
        """
        self.m_ready_to_active = True
