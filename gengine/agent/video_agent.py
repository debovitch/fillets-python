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
        self.draw_surface = None
        self.logical_size = (0, 0)
        self.output_rect = pygame.Rect(0, 0, 0, 0)
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
            
        draw_surface = self.draw_surface or self.screen

        # Fill the display and logical game surface with black as a background
        self.screen.fill((0, 0, 0))
        if draw_surface is not self.screen:
            draw_surface.fill((0, 0, 0))

        # If no drawers are registered, log error
        if not self.drawers:
            log_error("No drawers registered with the video agent")
        else:    
            # Draw all registered drawers
            self.draw_on(draw_surface)

        if draw_surface is not self.screen:
            if draw_surface.get_size() == self.output_rect.size:
                self.screen.blit(draw_surface, self.output_rect)
            else:
                scaled_surface = pygame.transform.scale(draw_surface, self.output_rect.size)
                self.screen.blit(scaled_surface, self.output_rect)
        
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
        fullscreen = options.get_as_bool("fullscreen", False)

        SysVideo.set_caption(options.get_param("caption", "Fish Fillets NG"))
        
        # Create or resize the screen if needed
        if (self.screen is None or 
                self.logical_size != (screen_width, screen_height) or
                self.fullscreen != fullscreen):
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
        fullscreen = options.get_as_bool("fullscreen", False)

        if fullscreen:
            if self.change_fullscreen_mode(screen_width, screen_height, screen_bpp):
                return

            log_warning(ExInfo("unable to use fullscreen resolution, trying windowed")
                       .add_info("width", screen_width)
                       .add_info("height", screen_height)
                       .add_info("bpp", screen_bpp))
            if options.get_as_bool("fullscreen", False):
                options.set_param("fullscreen", False)

        self.change_windowed_mode(screen_width, screen_height, screen_bpp)

    def change_fullscreen_mode(self, screen_width, screen_height, screen_bpp):
        """
        Use desktop fullscreen and scale the logical game surface into it.
        """
        display_size = self.get_fullscreen_size((screen_width, screen_height))
        try:
            self.screen = pygame.display.set_mode(
                display_size,
                self.get_video_flags() | pygame.FULLSCREEN,
                screen_bpp
            )
            self.fullscreen = True
            self.logical_size = (screen_width, screen_height)
            self.draw_surface = pygame.Surface(self.logical_size).convert()
            self.update_output_rect()
            self.center_mouse()
            return True
        except pygame.error:
            return False

    def change_windowed_mode(self, screen_width, screen_height, screen_bpp):
        """Set the normal windowed video mode."""
        try:
            self.screen = pygame.display.set_mode(
                (screen_width, screen_height),
                self.get_video_flags(),
                screen_bpp
            )
            self.fullscreen = False
            self.logical_size = (screen_width, screen_height)
            self.draw_surface = self.screen
            self.update_output_rect()
            self.center_mouse()
        except pygame.error as e:
            raise LogicException(ExInfo("Cannot set video mode")
                                .add_info("width", screen_width)
                                .add_info("height", screen_height)
                                .add_info("bpp", screen_bpp)
                                .add_info("error", str(e)))

    def get_fullscreen_size(self, fallback):
        """Return the desktop size for fullscreen, or fallback when unavailable."""
        if hasattr(pygame.display, "get_desktop_sizes"):
            sizes = pygame.display.get_desktop_sizes()
            if sizes:
                return sizes[0]

        info = pygame.display.Info()
        if info.current_w > 0 and info.current_h > 0:
            return info.current_w, info.current_h

        return fallback

    def update_output_rect(self):
        """Compute the scaled, centered output rectangle for the logical surface."""
        if self.logical_size == (0, 0) or not self.screen:
            self.output_rect = pygame.Rect(0, 0, 0, 0)
            return

        logical_width, logical_height = self.logical_size
        display_width = self.screen.get_width()
        display_height = self.screen.get_height()
        scale = min(display_width / logical_width, display_height / logical_height)
        output_width = max(1, int(logical_width * scale))
        output_height = max(1, int(logical_height * scale))
        self.output_rect = pygame.Rect(
            (display_width - output_width) // 2,
            (display_height - output_height) // 2,
            output_width,
            output_height,
        )
    
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
        Apply the current fullscreen option to the active display mode.
        """
        if self.screen:
            options = OptionAgent.agent()
            screen_width = options.get_as_int("screen_width", 640)
            screen_height = options.get_as_int("screen_height", 480)
            self.change_video_mode(screen_width, screen_height)
                
    def get_screen(self):
        """
        Get the logical game surface.
        
        Returns:
            pygame.Surface: The screen surface
        """
        return self.draw_surface or self.screen

    def screen_to_game_pos(self, pos):
        """
        Convert display coordinates to logical game coordinates.
        """
        if self.output_rect.width == 0 or self.output_rect.height == 0:
            return pos

        x = (pos[0] - self.output_rect.x) * self.logical_size[0] / self.output_rect.width
        y = (pos[1] - self.output_rect.y) * self.logical_size[1] / self.output_rect.height
        return int(x), int(y)

    def game_to_screen_pos(self, pos):
        """
        Convert logical game coordinates to display coordinates.
        """
        if self.logical_size == (0, 0):
            return pos

        x = self.output_rect.x + pos[0] * self.output_rect.width / self.logical_size[0]
        y = self.output_rect.y + pos[1] * self.output_rect.height / self.logical_size[1]
        return int(x), int(y)

    def center_mouse(self):
        """Move the mouse to the center of the logical game surface."""
        if self.logical_size != (0, 0):
            x = self.logical_size[0] // 2
            y = self.logical_size[1] // 2
            pygame.mouse.set_pos(self.game_to_screen_pos((x, y)))
        
    def get_mouse_pos(self):
        """
        Get the current mouse position.
        
        Returns:
            tuple: Mouse position (x, y)
        """
        return self.screen_to_game_pos(pygame.mouse.get_pos())
    
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
