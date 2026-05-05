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
game_functions.py - Python translation of game-script.cpp

Functions for the game Lua script interface.
These functions are registered with the Lua interpreter to allow Lua scripts
to interact with the game.
"""

from gengine.path import Path
from gengine.v2 import V2
from gengine.log import log_warning
from gengine.ex_info import ExInfo


def get_level_script(script_state):
    """
    Get the level script from the script state.
    
    Args:
        script_state: The script state
        
    Returns:
        LevelScript: The level script associated with the script
    """
    # In the Python version, we pass the level_script directly to the function
    return script_state


def get_model(script_state, model_index):
    """
    Get a model by its index.
    
    Args:
        script_state: The script state
        model_index: The model index
        
    Returns:
        Cube: The model
    """
    return get_level_script(script_state).get_model(model_index)


# ---- Game Functions ----

def game_set_room_waves(script_state, amp, periode, speed):
    """
    Set room waves.
    Lua: void game_setRoomWaves(amplitude, periode, speed)
    
    Args:
        script_state: The script state (LevelScript instance)
        amp: The wave amplitude
        periode: The wave periode
        speed: The wave speed
        
    Returns:
        int: Always 0
    """
    get_level_script(script_state).room().set_waves(amp, periode, speed)
    return 0


def game_add_model(script_state, kind, x, y, shape):
    """
    Add a model to the game.
    Lua: int game_addModel(kind, x, y, shape)
    
    Args:
        script_state: The script state (LevelScript instance)
        kind: The model kind
        x: The x coordinate
        y: The y coordinate
        shape: The model shape
        
    Returns:
        int: The model index
    """
    from level.model_factory import ModelFactory
    
    model = ModelFactory.create_model(kind, V2(x, y), shape)
    unit = ModelFactory.create_unit(kind)
    model_index = get_level_script(script_state).add_model(model, unit)
    
    return model_index


def game_get_cycles(script_state):
    """
    Get the game cycle count.
    Lua: int game_getCycles()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        int: The cycle count
    """
    cycles = get_level_script(script_state).room().get_cycles()
    return cycles


def game_add_decor(script_state, decor_name, *args):
    """
    Add decoration to the game.
    Lua: void game_addDecor(decor_name, params...)
    
    Args:
        script_state: The script state (LevelScript instance)
        decor_name: The decoration name
        *args: Additional parameters
        
    Returns:
        int: Always 0
    """
    if decor_name == "rope":
        model_index1, model_index2, shift_x1, shift_y1, shift_x2, shift_y2 = args
        
        model1 = get_model(script_state, model_index1)
        model2 = get_model(script_state, model_index2)
        
        from level.rope_decor import RopeDecor
        get_level_script(script_state).room().add_decor(
            RopeDecor(model1, model2, V2(shift_x1, shift_y1), V2(shift_x2, shift_y2)))
    else:
        log_warning(ExInfo("unknown decor").add_info("decor_name", decor_name))
    
    return 0


def game_set_screen_shift(script_state, x, y):
    """
    Set the screen shift.
    Lua: void game_setScreenShift(x, y)
    
    Args:
        script_state: The script state (LevelScript instance)
        x: The x shift
        y: The y shift
        
    Returns:
        int: Always 0
    """
    get_level_script(script_state).room().set_screen_shift(V2(x, y))
    return 0


def game_change_bg(script_state, picture):
    """
    Change the background picture.
    Lua: void game_changeBg(picture)
    
    Args:
        script_state: The script state (LevelScript instance)
        picture: The background picture
        
    Returns:
        int: Always 0
    """
    get_level_script(script_state).room().change_bg(picture)
    return 0


def game_get_bg(script_state):
    """
    Get the current background picture.
    Lua: string game_getBg()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        str: The background picture name
    """
    return get_level_script(script_state).room().get_bg()


def game_check_active(script_state):
    """
    Check for active fish, switch to non busy alive fish.
    Lua: void game_checkActive()
    
    Args:
        script_state: The script state (LevelScript instance)
        
    Returns:
        int: Always 0
    """
    get_level_script(script_state).room().check_active()
    return 0


def game_set_fast_falling(script_state, value):
    """
    Set fast falling for all objects.
    Lua: void game_setFastFalling(value)
    
    Args:
        script_state: The script state (LevelScript instance)
        value: Whether to enable fast falling
        
    Returns:
        int: Always 0
    """
    get_level_script(script_state).room().set_fast_falling(value)
    return 0


# ---- Model Functions ----

def model_add_anim(script_state, model_index, anim_name, picture, look_dir=0):
    """
    Add an animation to a model.
    Lua: void model_addAnim(model_index, anim_name, picture, lookDir)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        anim_name: The animation name
        picture: The animation picture
        look_dir: The look direction (0=left, 1=right)
        
    Returns:
        int: Always 0
    """
    from level.anim import Anim
    from level.shape_builder import ShapeBuilder
    
    model = get_model(script_state, model_index)
    if look_dir is None:
        look_dir = 0
    
    if not picture:
        model.anim.add_anim(anim_name, 
                          ShapeBuilder.create_image(model.shape, model.get_weight()),
                          look_dir)
    else:
        model.anim.add_anim(anim_name, Path.data_read_path(picture), look_dir)
    
    return 0


def model_run_anim(script_state, model_index, anim_name, phase=0):
    """
    Run an animation on a model.
    Lua: void model_runAnim(model_index, anim_name, phase=0)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        anim_name: The animation name
        phase: The animation phase
        
    Returns:
        int: Always 0
    """
    model = get_model(script_state, model_index)
    if phase is None:
        phase = 0
    model.anim.run_anim(anim_name, phase)
    return 0


def model_set_anim(script_state, model_index, anim_name, phase):
    """
    Set an animation on a model.
    Lua: void model_setAnim(model_index, anim_name, phase)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        anim_name: The animation name
        phase: The animation phase
        
    Returns:
        int: Always 0
    """
    model = get_model(script_state, model_index)
    if phase is None:
        phase = 0
    model.anim.set_anim(anim_name, phase)
    return 0


def model_use_special_anim(script_state, model_index, anim_name, phase):
    """
    Use a special animation on a model for one phase.
    Lua: void model_useSpecialAnim(model_index, anim_name, phase)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        anim_name: The animation name
        phase: The animation phase
        
    Returns:
        int: Always 0
    """
    model = get_model(script_state, model_index)
    if phase is None:
        phase = 0
    model.anim.use_special_anim(anim_name, phase)
    return 0


def model_count_anims(script_state, model_index, anim_name):
    """
    Count the number of animation phases.
    Lua: int model_countAnims(model_index, anim_name)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        anim_name: The animation name
        
    Returns:
        int: The number of animation phases
    """
    model = get_model(script_state, model_index)
    anims = model.anim.count_anim_phases(anim_name)
    return anims


def model_set_effect(script_state, model_index, effect_name):
    """
    Set a special view effect on a model.
    Lua: void model_setEffect(model_index, effect_name)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        effect_name: The effect name
        
    Returns:
        int: Always 0
    """
    model = get_model(script_state, model_index)
    model.anim.set_effect(effect_name)
    return 0


def model_get_loc(script_state, model_index):
    """
    Get the location of a model.
    Lua: (x, y) model_getLoc(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        tuple: The model location (x, y)
    """
    model = get_model(script_state, model_index)
    loc = model.get_location()
    return (loc.get_x(), loc.get_y())


def model_get_action(script_state, model_index):
    """
    Get the action of a model.
    Lua: string model_getAction(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        str: The model action
    """
    model = get_model(script_state, model_index)
    action = model.rules.get_action()
    return action


def model_get_state(script_state, model_index):
    """
    Get the state of a model.
    Lua: string model_getState(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        str: The model state
    """
    model = get_model(script_state, model_index)
    state = model.rules.get_state()
    return state


def model_get_dir(script_state, model_index):
    """
    Get the last move direction of a model.
    Lua: Dir::eDir model_getDir(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        int: The model direction
    """
    model = get_model(script_state, model_index)
    dir = model.get_last_move_dir()
    return dir.value


def model_get_touch_dir(script_state, model_index):
    """
    Get the touch direction of a model.
    Lua: Dir::eDir model_getTouchDir(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        int: The touch direction
    """
    model = get_model(script_state, model_index)
    dir = model.rules.get_touch_dir()
    return dir.value


def model_is_alive(script_state, model_index):
    """
    Check if a model is alive.
    Lua: bool model_isAlive(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        bool: True if the model is alive
    """
    model = get_model(script_state, model_index)
    alive = model.is_alive()
    return alive


def model_is_out(script_state, model_index):
    """
    Check if a model is out of the room.
    Lua: bool model_isOut(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        bool: True if the model is out of the room
    """
    model = get_model(script_state, model_index)
    out = model.is_out()
    return out


def model_is_left(script_state, model_index):
    """
    Check if a model is looking left.
    Lua: bool model_isLeft(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        bool: True if the model is looking left
    """
    model = get_model(script_state, model_index)
    left = model.is_left()
    return left


def model_is_at_border(script_state, model_index):
    """
    Check if a model is at the room border.
    Lua: bool model_isAtBorder(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        bool: True if the model is at the room border
    """
    model = get_model(script_state, model_index)
    at_border = model.rules.is_at_border()
    return at_border


def model_get_w(script_state, model_index):
    """
    Get the width of a model.
    Lua: int model_getW(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        int: The model width
    """
    model = get_model(script_state, model_index)
    width = model.shape.get_w()
    return width


def model_get_h(script_state, model_index):
    """
    Get the height of a model.
    Lua: int model_getH(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        int: The model height
    """
    model = get_model(script_state, model_index)
    height = model.shape.get_h()
    return height


def model_set_goal(script_state, model_index, goalname):
    """
    Set the goal of a model.
    Lua: void model_setGoal(model_index, goalname)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        goalname: The goal name
        
    Returns:
        int: Always 0
    """
    from level.goal import Goal
    
    model = get_model(script_state, model_index)
    goal = Goal.no_goal()
    
    if goalname == "goal_no":
        goal = Goal.no_goal()
    elif goalname == "goal_out":
        goal = Goal.out_goal()
    elif goalname == "goal_escape":
        goal = Goal.escape_goal()
    elif goalname == "goal_alive":
        goal = Goal.alive_goal()
    else:
        error = ExInfo("unknown goal").add_info("goal", goalname)
        log_warning(error)
        raise ValueError(error.info())
    
    model.set_goal(goal)
    return 0


def model_change_turn_side(script_state, model_index):
    """
    Change the side a model is looking.
    Lua: void model_change_turnSide(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        int: Always 0
    """
    model = get_model(script_state, model_index)
    model.change_turn_side()
    return 0


def model_change_set_location(script_state, model_index, x, y):
    """
    Change the location of a model.
    Lua: void model_change_setLocation(model_index, x, y)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        x: The x coordinate
        y: The y coordinate
        
    Returns:
        int: Always 0
    """
    model = get_model(script_state, model_index)
    model.rules.change_set_location(V2(x, y))
    return 0


def model_set_view_shift(script_state, model_index, shift_x, shift_y):
    """
    Set the view shift of a model.
    Lua: void model_setViewShift(model_index, shift_x, shift_y)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        shift_x: The x shift
        shift_y: The y shift
        
    Returns:
        int: Always 0
    """
    model = get_model(script_state, model_index)
    model.anim.set_view_shift(V2(shift_x, shift_y))
    return 0


def model_get_view_shift(script_state, model_index):
    """
    Get the view shift of a model.
    Lua: shift_x, shift_y model_getViewShift(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        tuple: The view shift (shift_x, shift_y)
    """
    model = get_model(script_state, model_index)
    shift = model.anim.get_view_shift()
    return (shift.get_x(), shift.get_y())


def model_set_busy(script_state, model_index, busy):
    """
    Set whether a model is busy.
    Lua: void model_setBusy(model_index, value)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        busy: Whether the model is busy
        
    Returns:
        int: Always 0
    """
    model = get_model(script_state, model_index)
    model.set_busy(busy)
    return 0


def model_get_extra_params(script_state, model_index):
    """
    Get the extra parameters of a model.
    Lua: table model_getExtraParams(model_index)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        
    Returns:
        dict: The extra parameters
    """
    model = get_model(script_state, model_index)
    
    params = script_state.level.script.state.table()
    params["outDir"] = model.get_out_dir().value
    params["outCapacity"] = model.get_out_capacity()
    params["weight"] = model.get_weight().value
    params["anim"] = model.anim.get_state()

    return params


def model_change_set_extra_params(script_state, model_index, params):
    """
    Set the extra parameters of a model.
    Lua: void model_change_setExtraParams(model_index, table)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        params: The extra parameters
        
    Returns:
        int: Always 0
    """
    from level.dir import Dir
    from level.cube import Cube
    
    model = get_model(script_state, model_index)
    
    out_dir = Dir(params["outDir"])
    out_capacity = params["outCapacity"]
    weight = Cube.Weight(params["weight"])
    anim_state = params["anim"]
    
    model.set_out_dir(out_dir, out_capacity, weight)
    model.set_extra_params()
    model.anim.restore_state(anim_state)
    
    return 0


def model_equals(script_state, model_index, x, y):
    """
    Check if an object at a location equals a model.
    Lua: bool model_equals(model_index, x, y)
    
    Args:
        script_state: The script state (LevelScript instance)
        model_index: The model index
        x: The x coordinate
        y: The y coordinate
        
    Returns:
        bool: True if the object equals the model
    """
    other = get_level_script(script_state).ask_field(V2(x, y))
    
    equals = False
    if other:
        if model_index == -1:
            equals = False
        else:
            equals = (model_index == other.get_index())
    else:
        if model_index == -1:
            equals = True
    
    return equals


# ---- Sound Functions ----

def sound_add_sound(script_state, name, file):
    """
    Add a sound.
    Lua: void sound_addSound(name, file)
    
    Args:
        script_state: The script state (LevelScript instance)
        name: The sound name
        file: The sound file
        
    Returns:
        int: Always 0
    """
    get_level_script(script_state).add_sound(name, Path.data_read_path(file))
    return 0


def sound_play_sound(script_state, name, volume=100):
    """
    Play a sound.
    Lua: void sound_playSound(name, volume)
    
    Args:
        script_state: The script state (LevelScript instance)
        name: The sound name
        volume: The sound volume
        
    Returns:
        int: Always 0
    """
    get_level_script(script_state).play_sound(name, volume)
    return 0


# Register all functions with the Lua interpreter
def register_lua_functions(script_agent, level_script):
    """
    Register all game functions with the Lua interpreter.
    
    Args:
        script_agent: The script agent
        level_script: The level script
    """
    script = script_agent.script
    
    # Register game functions
    script.register_function("game_setRoomWaves", lambda state, *args: game_set_room_waves(level_script, *args))
    script.register_function("game_addModel", lambda state, *args: game_add_model(level_script, *args))
    script.register_function("game_getCycles", lambda state, *args: game_get_cycles(level_script))
    script.register_function("game_addDecor", lambda state, *args: game_add_decor(level_script, *args))
    script.register_function("game_setScreenShift", lambda state, *args: game_set_screen_shift(level_script, *args))
    script.register_function("game_changeBg", lambda state, *args: game_change_bg(level_script, *args))
    script.register_function("game_getBg", lambda state, *args: game_get_bg(level_script))
    script.register_function("game_checkActive", lambda state, *args: game_check_active(level_script))
    script.register_function("game_setFastFalling", lambda state, *args: game_set_fast_falling(level_script, *args))
    
    # Register model functions
    script.register_function("model_addAnim", lambda state, *args: model_add_anim(level_script, *args))
    script.register_function("model_runAnim", lambda state, *args: model_run_anim(level_script, *args))
    script.register_function("model_setAnim", lambda state, *args: model_set_anim(level_script, *args))
    script.register_function("model_useSpecialAnim", lambda state, *args: model_use_special_anim(level_script, *args))
    script.register_function("model_countAnims", lambda state, *args: model_count_anims(level_script, *args))
    script.register_function("model_setEffect", lambda state, *args: model_set_effect(level_script, *args))
    script.register_function("model_getLoc", lambda state, *args: model_get_loc(level_script, *args))
    script.register_function("model_getAction", lambda state, *args: model_get_action(level_script, *args))
    script.register_function("model_getState", lambda state, *args: model_get_state(level_script, *args))
    script.register_function("model_getDir", lambda state, *args: model_get_dir(level_script, *args))
    script.register_function("model_getTouchDir", lambda state, *args: model_get_touch_dir(level_script, *args))
    script.register_function("model_isAlive", lambda state, *args: model_is_alive(level_script, *args))
    script.register_function("model_isOut", lambda state, *args: model_is_out(level_script, *args))
    script.register_function("model_isLeft", lambda state, *args: model_is_left(level_script, *args))
    script.register_function("model_isAtBorder", lambda state, *args: model_is_at_border(level_script, *args))
    script.register_function("model_getW", lambda state, *args: model_get_w(level_script, *args))
    script.register_function("model_getH", lambda state, *args: model_get_h(level_script, *args))
    script.register_function("model_setGoal", lambda state, *args: model_set_goal(level_script, *args))
    script.register_function("model_change_turnSide", lambda state, *args: model_change_turn_side(level_script, *args))
    script.register_function("model_change_setLocation", lambda state, *args: model_change_set_location(level_script, *args))
    script.register_function("model_setViewShift", lambda state, *args: model_set_view_shift(level_script, *args))
    script.register_function("model_getViewShift", lambda state, *args: model_get_view_shift(level_script, *args))
    script.register_function("model_setBusy", lambda state, *args: model_set_busy(level_script, *args))
    script.register_function("model_getExtraParams", lambda state, *args: model_get_extra_params(level_script, *args))
    script.register_function("model_change_setExtraParams", lambda state, *args: model_change_set_extra_params(level_script, *args))
    script.register_function("model_equals", lambda state, *args: model_equals(level_script, *args))
    
    # Register sound functions
    script.register_function("sound_addSound", lambda state, *args: sound_add_sound(level_script, *args))
    script.register_function("sound_playSound", lambda state, *args: sound_play_sound(level_script, *args))
