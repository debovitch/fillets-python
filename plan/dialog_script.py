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
Script interface for dialogs.
"""

from gengine.path import Path
from gengine.color import Color
from plan.subtitle_agent import SubTitleAgent
from gengine.agent.sound_agent import SoundAgent

class DialogScript:
    """Handlers for dialog-related script functions."""
    
    @staticmethod
    def register(script_state, planner):
        """
        Register dialog script functions to the Lua state.
        
        Args:
            script_state: The script state to register functions with
            planner: The planner to use for script functions
        """
        # Store planner reference for static methods
        DialogScript.planner = planner
        
        # Register game action functions
        script_state.register_function("game_planAction", DialogScript.game_plan_action)
        script_state.register_function("game_isPlanning", DialogScript.game_is_planning)
        script_state.register_function("game_killPlan", DialogScript.game_kill_plan)
        
        # Register dialog functions
        script_state.register_function("dialog_isDialog", DialogScript.dialog_is_dialog)
        script_state.register_function("dialog_addFont", DialogScript.dialog_add_font)
        script_state.register_function("dialog_addDialog", DialogScript.dialog_add_dialog)
        script_state.register_function("model_isTalking", DialogScript.model_is_talking)
        script_state.register_function("model_talk", DialogScript.model_talk)
        script_state.register_function("model_killSound", DialogScript.model_kill_sound)
        
        # Register sound functions
        script_state.register_function("sound_playMusic", DialogScript.sound_play_music)
        script_state.register_function("sound_stopMusic", DialogScript.sound_stop_music)
    
    @staticmethod
    def game_plan_action(script_state, func_ref):
        """
        Plan a new game action.
        
        Args:
            script_state: The script state
            func_ref: The function reference to execute
            
        Returns:
            None
        """
        DialogScript.planner.plan_action(script_state, func_ref)
        return None
    
    @staticmethod
    def game_is_planning(script_state):
        """
        Check if there are any planned actions.
        
        Args:
            script_state: The script state
            
        Returns:
            bool: True if there are planned actions
        """
        return DialogScript.planner.is_planning()
    
    @staticmethod
    def game_kill_plan(script_state):
        """
        Interrupt the current plan.
        
        Args:
            script_state: The script state
            
        Returns:
            None
        """
        DialogScript.planner.interrupt_plan()
        return None
    
    @staticmethod
    def dialog_is_dialog(script_state):
        """
        Check if there is currently a dialog.
        
        Args:
            script_state: The script state
            
        Returns:
            bool: True if there is a dialog
        """
        return DialogScript.planner.dialogs().is_dialog()
    
    @staticmethod
    def dialog_add_font(script_state, name, red, green, blue):
        """
        Add a new font for subtitles.
        
        Args:
            script_state: The script state
            name (str): The font name
            red (int): The red component (0-255)
            green (int): The green component (0-255)
            blue (int): The blue component (0-255)
            
        Returns:
            None
        """
        SubTitleAgent.get_instance().add_font(name, Color(red, green, blue))
        return None
    
    @staticmethod
    def dialog_add_dialog(script_state, name, lang, soundfile, fontname="", subtitle=""):
        """
        Add a new dialog.
        
        Args:
            script_state: The script state
            name (str): The dialog name
            lang (str): The language code
            soundfile (str): The sound file path
            fontname (str, optional): The font name to use
            subtitle (str, optional): The subtitle text
            
        Returns:
            None
        """
        from gengine.resource.dialog import Dialog
        dialog = Dialog(lang, soundfile, subtitle)
        dialog.fontname = fontname
        DialogScript.planner.dialogs().add_dialog(name, dialog)
        return None
    
    @staticmethod
    def model_is_talking(script_state, model_index):
        """
        Check if a model is currently talking.
        
        Args:
            script_state: The script state
            model_index (int): The model index
            
        Returns:
            bool: True if the model is talking
        """
        return DialogScript.planner.dialogs().is_talking(model_index)
    
    @staticmethod
    def model_talk(script_state, model_index, name, volume=75, loops=0, dialog_flag=False):
        """
        Make a model talk.
        
        Args:
            script_state: The script state
            model_index (int): The model index
            name (str): The dialog name
            volume (int, optional): The volume (0-100)
            loops (int, optional): Number of times to repeat
            dialog_flag (bool, optional): Whether this is a dialog
            
        Returns:
            None
        """
        if volume is None:
            volume = 75
        if loops is None:
            loops = 0
        if dialog_flag is None:
            dialog_flag = False

        DialogScript.planner.dialogs().actor_talk(model_index, name, volume, loops, dialog_flag)
        return None
    
    @staticmethod
    def model_kill_sound(script_state, model_index):
        """
        Stop a model from talking.
        
        Args:
            script_state: The script state
            model_index (int): The model index
            
        Returns:
            None
        """
        DialogScript.planner.dialogs().kill_sound(model_index)
        return None
    
    @staticmethod
    def sound_play_music(script_state, music_name):
        """
        Play a music file.
        
        Args:
            script_state: The script state
            music_name (str): The music file name
            
        Returns:
            None
        """
        SoundAgent.get_instance().play_music(Path.data_read_path(music_name), None)
        return None
    
    @staticmethod
    def sound_stop_music(script_state):
        """
        Stop the currently playing music.
        
        Args:
            script_state: The script state
            
        Returns:
            None
        """
        SoundAgent.get_instance().stop_music()
        return None
