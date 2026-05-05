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
import sys
from gengine.agent.base_agent import BaseAgent, agent_class
from gengine.name import Name
from gengine.multi_drawer import MultiDrawer
from gengine.sys_video import SysVideo
from gengine.path import Path
from gengine.log import log_debug, log_warning, log_error
from gengine.ex_info import ExInfo
from gengine.exceptions import LogicException
from gengine.agent.option_agent import OptionAgent
from gengine.exceptions import UnknownMsgException

@agent_class(Name.VIDEO_NAME)
class VideoAgent(BaseAgent, MultiDrawer):
    """
    Video agent initializes the video mode and manages the display.
    Every cycle lets registered drawers draw on the screen.
    """
    
    def __init__(self):
        """
        Initialize the video agent.
        """
        BaseAgent.__init__(self)
        MultiDrawer.__init__(self)
        self.screen = None
        self.fullscreen = False
    
    def own_init(self):
        """
        Initialize the graphics window.
        Register watcher for "fullscreen" and "screen_*" options.
        """
        # Initialize pygame's video subsystem
        if not pygame.get_init():
            pygame.init()
        
        self.fullscreen = False
        
        # Set the icon
        self.set_icon(Path.data_read_path("images/icon.png"))
        
        # Register to watch for fullscreen changes
        self.register_watcher("fullscreen")
        
        # Initialize the video mode
        self.init_video_mode()
    
    def own_update(self):
        """
        Draw all drawers from the list.
        First will be drawn first.
        """
        # Check if screen is valid
        if not self.screen:
            # log_debug("Screen is not initialized in own_update")
            return
            
        # Fill the screen with black as a background
        self.screen.fill((0, 0, 0))
        
        # If no drawers are registered, log error
        if not self.drawers:
            log_error("No drawers registered with the video agent")
        else:    
            # Draw all registered drawers
            self.draw_on(self.screen)
        
        # Update the display
        pygame.display.flip()
    
    def own_shutdown(self):
        """
        Shutdown Pygame.
        """
        pygame.quit()
    
    def set_icon(self, file_path):
        """
        Load and set the window icon.
        
        Args:
            file_path (Path): The path to the icon file
        """
        try:
            icon = pygame.image.load(file_path.get_native())
            pygame.display.set_icon(icon)
        except pygame.error as e:
            log_debug(ExInfo("Cannot load icon").add_info("file", file_path.get_native()).add_info("error", str(e)))
    
    def init_video_mode(self):
        """
        Initialize the video mode according to options.
        Change window only when necessary.
        """
        options = OptionAgent.agent()
        screen_width = options.get_as_int("screen_width", 640)
        screen_height = options.get_as_int("screen_height", 480)
        
        SysVideo.set_caption(options.get_param("caption", "Fish Fillets NG"))
        
        # Create or resize the screen if needed
        if (self.screen is None or 
                self.screen.get_width() != screen_width or 
                self.screen.get_height() != screen_height):
            self.change_video_mode(screen_width, screen_height)
    
    def change_video_mode(self, screen_width, screen_height):
        """
        Initialize a new video mode.
        
        Args:
            screen_width (int): The screen width
            screen_height (int): The screen height
        """
        options = OptionAgent.agent()
        screen_bpp = options.get_as_int("screen_bpp", 32)
        video_flags = self.get_video_flags()
        self.fullscreen = options.get_as_bool("fullscreen", False)
        
        if self.fullscreen:
            video_flags |= pygame.FULLSCREEN
        
        try:
            # Try to set the video mode
            self.screen = pygame.display.set_mode(
                (screen_width, screen_height), 
                video_flags, 
                screen_bpp
            )
            
            # Center the mouse pointer
            pygame.mouse.set_pos(screen_width // 2, screen_height // 2)
            
        except pygame.error as e:
            if video_flags & pygame.FULLSCREEN:
                log_warning(ExInfo("unable to use fullscreen resolution, trying windowed")
                           .add_info("width", screen_width)
                           .add_info("height", screen_height)
                           .add_info("bpp", screen_bpp))
                
                # Try again without fullscreen
                video_flags &= ~pygame.FULLSCREEN
                try:
                    self.screen = pygame.display.set_mode(
                        (screen_width, screen_height), 
                        video_flags, 
                        screen_bpp
                    )
                    # Center the mouse pointer
                    pygame.mouse.set_pos(screen_width // 2, screen_height // 2)
                except pygame.error as e2:
                    raise LogicException(ExInfo("Cannot set video mode")
                                        .add_info("width", screen_width)
                                        .add_info("height", screen_height)
                                        .add_info("bpp", screen_bpp)
                                        .add_info("error", str(e2)))
            else:
                raise LogicException(ExInfo("Cannot set video mode")
                                    .add_info("width", screen_width)
                                    .add_info("height", screen_height)
                                    .add_info("bpp", screen_bpp)
                                    .add_info("error", str(e)))
    
    def get_video_flags(self):
        """
        Obtain video information about the best video mode.
        
        Returns:
            int: The best video flags for pygame
        """
        video_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        return video_flags
    
    def toggle_fullscreen(self):
        """
        Toggle fullscreen mode.
        """
        try:
            # Try to toggle fullscreen
            pygame.display.toggle_fullscreen()
            self.fullscreen = not self.fullscreen
        except pygame.error:
            # If toggle fails, reinitialize the video mode
            if self.screen:
                self.change_video_mode(self.screen.get_width(), self.screen.get_height())
                
    def get_screen(self):
        """
        Get the screen surface.
        
        Returns:
            pygame.Surface: The screen surface
        """
        return self.screen
        
    def get_mouse_pos(self):
        """
        Get the current mouse position.
        
        Returns:
            tuple: Mouse position (x, y)
        """
        return pygame.mouse.get_pos()
    
    def receive_simple(self, msg):
        """
        Handle simple messages.
        
        Args:
            msg (SimpleMsg): The message to handle
            
        Raises:
            UnknownMsgException: If the message cannot be handled
        """
        if msg.equals_name("fullscreen"):
            options = OptionAgent.agent()
            toggle = not options.get_as_bool("fullscreen")
            options.set_persistent("fullscreen", toggle)
        else:
            super().receive_simple(msg)
    
    def receive_string(self, msg):
        """
        Handle string messages.
        
        Args:
            msg (StringMsg): The message to handle
            
        Raises:
            UnknownMsgException: If the message cannot be handled
        """
        if msg.equals_name("param_changed"):
            param = msg.get_value()
            if param == "fullscreen":
                fs = OptionAgent.agent().get_as_bool("fullscreen")
                if fs != self.fullscreen:
                    self.toggle_fullscreen()
            else:
                super().receive_string(msg)
        else:
            super().receive_string(msg)