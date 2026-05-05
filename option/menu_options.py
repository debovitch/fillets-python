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
from gengine.path import Path
from gengine.agent.option_agent import OptionAgent
from gengine.agent.video_agent import VideoAgent
from gengine.mouse_stroke import MouseStroke
from gengine.message.simple_msg import SimpleMsg
from gengine.message.string_msg import StringMsg
from gengine.drawable import Drawable
from gengine.v2 import V2
from gengine.exceptions import UnknownMsgException
from plan.game_state import GameState

from widget.h_box import HBox
from widget.v_box import VBox
from widget.wi_picture import WiPicture
from widget.wi_space import WiSpace
from widget.wi_button import WiButton
from widget.wi_status_bar import WiStatusBar
from widget.slider import Slider
from widget.radio_box import RadioBox
from option.select_lang import SelectLang
from option.options_input import OptionsInput

class MenuOptions(GameState, Drawable):
    """
    Options menu which allows setting language and tuning volume.
    """
    
    def __init__(self):
        """
        Initialize options menu.
        """
        super().__init__()
        self.container = None
        self.status_bar = None
        self.need_refresh = False
        self.drawer = None
        
        # Set up input handler
        self.take_handler(OptionsInput(self))
        
        # Create and register drawable
        self.prepare_menu()
    
    def get_name(self):
        """
        Get state name.
        
        Returns:
            str: State name
        """
        return "state_options"
    
    def allow_bg(self):
        """
        Allow background.
        
        Returns:
            bool: True if background is allowed
        """
        return True
    
    def own_init_state(self):
        """
        Initialize state.
        """
        # Register for language changes to refresh UI
        self.register_watcher("lang")
        self.own_resume_state()
    
    def own_resume_state(self):
        """
        Resume state.
        """
        if not self.container:
            return
            
        # Center container on screen
        content_w = self.container.get_w()
        content_h = self.container.get_h()
        options = OptionAgent.agent()
        screen_w = options.get_as_int("screen_width")
        screen_h = options.get_as_int("screen_height")
        
        self.container.set_shift(
            V2((screen_w - content_w) // 2, (screen_h - content_h) // 2)
        )
    
    def own_update_state(self):
        """
        Update state.
        """
        if self.need_refresh:
            self.need_refresh = False
            self.prepare_menu()
            self.own_resume_state()
        
        # Update tooltip
        if self.container and self.status_bar and self.get_input():
            mouse_loc = self.get_input().get_mouse_loc()
            if mouse_loc:
                tooltip = self.container.get_tip(mouse_loc)
                self.status_bar.set_label(tooltip)
    
    def own_pause_state(self):
        """
        Pause state.
        """
        pass
    
    def own_clean_state(self):
        """
        Clean up state.
        """
        OptionAgent.agent().remove_watchers(self.get_name())
    
    def prepare_menu(self):
        """
        Prepare options menu.
        """
        if self.container:
            if self.drawer:
                self.deregister_drawable(self.container)
            self.container = None
        
        # Load labels
        # TODO: Implement Labels class
        # For now use a simple dict
        labels = {
            "menu_sound": "Sound volume",
            "menu_music": "Music volume",
            "menu_lang": "Language",
            "menu_speech": "Speech language",
            "menu_subtitles": "Subtitles",
            "menu_back": "Back to game"
        }
        
        sound_box = self.create_sound_panel(labels)
        music_box = self.create_music_panel(labels)
        
        vbox = VBox()
        vbox.add_widget(sound_box)
        vbox.add_widget(WiSpace(0, 10))
        vbox.add_widget(music_box)
        vbox.add_widget(WiSpace(0, 10))
        vbox.add_widget(self.create_lang_panel(labels))
        vbox.add_widget(WiSpace(0, 5))
        vbox.add_widget(self.create_speech_panel(labels))
        vbox.add_widget(WiSpace(0, 5))
        vbox.add_widget(self.create_subtitles_panel(labels))
        
        back_button = self.create_back_button(labels)
        self.status_bar = self.create_status_bar(music_box.get_w() - back_button.get_w())
        
        back_box = HBox()
        back_box.add_widget(self.status_bar)
        back_box.add_widget(back_button)
        
        vbox.add_widget(back_box)
        self.container = vbox
        
        # Register as drawable
        if self.drawer:
            self.register_drawable(self.container)
    
    def create_sound_panel(self, labels):
        """
        Create sound volume panel.
        
        Args:
            labels (dict): Label dictionary
            
        Returns:
            HBox: Sound panel
        """
        sound_box = HBox()
        sound_box.add_widget(WiPicture(
            Path.data_read_path("images/menu/volume_sound.png")))
        sound_box.add_widget(WiSpace(10, 0))
        sound_box.add_widget(Slider("volume_sound", 0, 100))
        sound_box.set_tip(labels["menu_sound"])
        return sound_box
    
    def create_music_panel(self, labels):
        """
        Create music volume panel.
        
        Args:
            labels (dict): Label dictionary
            
        Returns:
            HBox: Music panel
        """
        music_box = HBox()
        music_box.add_widget(WiPicture(
            Path.data_read_path("images/menu/volume_music.png")))
        music_box.add_widget(WiSpace(10, 0))
        music_box.add_widget(Slider("volume_music", 0, 100))
        music_box.set_tip(labels["menu_music"])
        return music_box
    
    def create_lang_panel(self, labels):
        """
        Create language panel.
        
        Args:
            labels (dict): Label dictionary
            
        Returns:
            HBox: Language panel
        """
        lang_box = HBox()
        path = Path.data_read_path("images/menu/lang.png")
        if path.exists():
            lang_box.add_widget(WiPicture(path))
            lang_box.add_widget(WiSpace(10, 0))
            
            script_path = Path.data_read_path("script/select_lang.lua")
            if script_path.exists():
                lang_box.add_widget(SelectLang("lang", script_path))
            else:
                # Fallback if script doesn't exist
                dummy_box = HBox()
                dummy_box.add_widget(WiSpace(100, 30))
                lang_box.add_widget(dummy_box)
                
            lang_box.set_tip(labels["menu_lang"])
        return lang_box
    
    def create_speech_panel(self, labels):
        """
        Create speech panel.
        
        Args:
            labels (dict): Label dictionary
            
        Returns:
            HBox: Speech panel
        """
        speech_box = HBox()
        path = Path.data_read_path("images/menu/speech.png")
        if path.exists():
            speech_box.add_widget(WiPicture(path))
            speech_box.add_widget(WiSpace(10, 0))
            
            script_path = Path.data_read_path("script/select_speech.lua")
            if script_path.exists():
                speech_box.add_widget(SelectLang("speech", script_path))
            else:
                # Fallback if script doesn't exist
                dummy_box = HBox()
                dummy_box.add_widget(WiSpace(100, 30))
                speech_box.add_widget(dummy_box)
                
            speech_box.set_tip(labels["menu_speech"])
        return speech_box
    
    def create_subtitles_panel(self, labels):
        """
        Create subtitles panel.
        
        Args:
            labels (dict): Label dictionary
            
        Returns:
            HBox: Subtitles panel
        """
        choose_box = HBox()
        path = Path.data_read_path("images/menu/subtitle.png")
        if path.exists():
            choose_box.add_widget(WiPicture(path))
            choose_box.add_widget(WiSpace(10, 0))
            
            yes_path = Path.data_read_path("images/menu/subtitles/yes.png")
            no_path = Path.data_read_path("images/menu/subtitles/no.png")
            
            if yes_path.exists() and no_path.exists():
                choose_box.add_widget(RadioBox("subtitles", "1", yes_path))
                choose_box.add_widget(RadioBox("subtitles", "0", no_path))
            else:
                # Fallback if images don't exist
                dummy_box = HBox()
                dummy_box.add_widget(WiSpace(100, 30))
                choose_box.add_widget(dummy_box)
                
            choose_box.set_tip(labels["menu_subtitles"])
        return choose_box
    
    def create_back_button(self, labels):
        """
        Create back button.
        
        Args:
            labels (dict): Label dictionary
            
        Returns:
            WiButton: Back button
        """
        path = Path.data_read_path("images/menu/back.png")
        if path.exists():
            button = WiButton(
                WiPicture(path),
                SimpleMsg(self, "quit"))
            button.set_tip(labels["menu_back"])
            return button
        else:
            # Fallback if image doesn't exist
            space = WiSpace(100, 30)
            return space
    
    def create_status_bar(self, width):
        """
        Create status bar.
        
        Args:
            width (int): Status bar width
            
        Returns:
            WiStatusBar: Status bar
        """
        color = (0, 255, 0)
        
        # Try to load font
        font_path = Path.data_read_path("font/font_menu.ttf")
        if font_path.exists():
            font = pygame.font.Font(font_path.get_native(), 16)
        else:
            # Fallback to system font
            font = pygame.font.SysFont("Arial", 16)
            
        return WiStatusBar(font, color, width)
    
    def mouse_button(self, stroke):
        """
        Handle mouse button.
        
        Args:
            stroke (MouseStroke): Mouse button event
        """
        if self.container:
            self.container.mouse_button(stroke)
    
    def draw_on(self, screen):
        """
        Draw options menu background.
        
        Args:
            screen (pygame.Surface): Surface to draw on
        """
        if pygame.SRCALPHA:
            # Match the original C++ menu veil: white with about 50% opacity.
            s = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            s.fill((0xf0, 0xf0, 0xf0, 129))
            screen.blit(s, (0, 0))
        else:
            # Fallback for older Pygame versions
            overlay_color = (0xf0, 0xf0, 0xf0)
            s = pygame.Surface((screen.get_width(), screen.get_height()))
            s.fill(overlay_color)
            s.set_alpha(129)
            screen.blit(s, (0, 0))

        if self.container:
            self.container.draw_on(screen)

    def receive_simple(self, msg):
        """
        Handle simple message.

        Args:
            msg (SimpleMsg): Simple message

        Raises:
            UnknownMsgException: If message is unknown
        """
        if msg.equals_name("quit"):
            self.quit_state()
        else:
            raise UnknownMsgException(msg)
    
    def receive_string(self, msg):
        """
        Handle string message.
        
        Args:
            msg (StringMsg): String message
            
        Raises:
            UnknownMsgException: If message is unknown
        """
        if msg.equals_name("param_changed"):
            param = msg.get_value()
            if param == "lang":
                self.need_refresh = True
        else:
            raise UnknownMsgException(msg)
    
    def register_watcher(self, name):
        """
        Register a watcher for parameter changes.
        
        Args:
            name (str): Parameter name
        """
        msg = StringMsg(self, "param_changed", name)
        OptionAgent.agent().add_watcher(name, msg)
