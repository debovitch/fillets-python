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
from typing import Optional
import pygame.gfxdraw
from gengine.v2 import V2
from gengine.no_copy import NoCopy
from gengine.resource.res_image_pack import ResImagePack
from gengine.path import Path
from gengine.agent.timer_agent import TimerAgent

class NodeDrawer(NoCopy):
    """
    Drawer that knows how to draw nodes on the world map.
    """
    
    def __init__(self):
        """Initialize a new node drawer."""
        # Import here to avoid circular imports
        from menu.level_node import LevelNode
        
        # Load the font
        pygame.font.init()
        self.font = pygame.font.Font(Path.data_read_path("font/font_menu.ttf").get_native(), 22)
        
        # Initialize the image pack
        self.image_pack = ResImagePack()
        
        # Add the node images
        self.image_pack.add_image("solved", Path.data_read_path("images/menu/n0.png"))
        
        # Add the open node images
        self.image_pack.add_image("open", Path.data_read_path("images/menu/n1.png"))
        self.image_pack.add_image("open", Path.data_read_path("images/menu/n2.png"))
        self.image_pack.add_image("open", Path.data_read_path("images/menu/n3.png"))
        self.image_pack.add_image("open", Path.data_read_path("images/menu/n4.png"))
        
        # Add the far node image
        self.image_pack.add_image("far", Path.data_read_path("images/menu/n_far.png"))
        
        # Reference to screen surface
        self.screen = None

    def __del__(self):
        """Release loaded node images."""
        self.clean()

    def clean(self):
        """Release resources held by the drawer."""
        if self.image_pack:
            self.image_pack.remove_all()
            self.image_pack = None
        self.font = None
        self.screen = None
    
    def set_screen(self, screen: pygame.Surface) -> None:
        """
        Set the screen to draw on.
        
        Args:
            screen: The screen surface
        """
        self.screen = screen
    
    def draw_node(self, node) -> None:
        """
        Draw blinking dot centered on node position.
        
        Args:
            node: The node to draw
        """
        from menu.level_node import LevelNode
        
        if not self.screen:
            return
            
        loc = node.get_loc()
        self.draw_dot(self.image_pack.get_res("far"), loc)
        
        dot = None
        node_state = node.get_state()
        
        if node_state == LevelNode.STATE_FAR:
            return
        elif node_state == LevelNode.STATE_OPEN:
            # Calculate animation phase for blinking effect
            phase = TimerAgent.agent().get_cycles() % 10
            if phase > 4:
                phase -= 1
            if phase > 7:
                phase -= 1
            if phase >= 4:
                phase = 7 - phase
                
            dot = self.image_pack.get_res("open", phase)
        elif node_state == LevelNode.STATE_SOLVED:
            dot = self.image_pack.get_res("solved")
        else:
            # Unknown state - log warning
            from gengine.log import log_warning
            from gengine.ex_info import ExInfo
            log_warning(ExInfo("don't know how to draw node").add_info("state", node_state))
            return
            
        self.draw_dot(dot, loc)
    
    def draw_dot(self, dot, loc: V2) -> None:
        """
        Draw centered dot.
        
        Args:
            dot: The dot surface
            loc: The location (center point)
        """
        if not self.screen:
            return
            
        rect = pygame.Rect(
            loc.get_x() - dot.get_width() // 2,
            loc.get_y() - dot.get_height() // 2,
            dot.get_width(),
            dot.get_height()
        )
        self.screen.blit(dot, rect)
    
    def draw_select(self, loc: V2) -> None:
        """
        Highlights selected node.
        
        Args:
            loc: The location
        """
        if not self.screen:
            return
            
        dot = self.image_pack.get_res("solved")
        radius = max(dot.get_width(), dot.get_height()) // 2 + 1
        
        # Convert RGBA color 0xffc61880 to pygame color format
        # RGBA in original: 255, 198, 24, 128
        color = (255, 198, 24, 128)
        
        # Draw filled circle
        pygame.gfxdraw.filled_circle(
            self.screen, 
            int(loc.get_x()), 
            int(loc.get_y()), 
            radius, 
            color
        )
    
    def draw_selected(self, level_name: str) -> None:
        """
        Draws name of selected level.
        
        Args:
            level_name: The level name
        """
        if not self.screen or not self.font:
            return
            
        # Calculate text width
        text_width = self.font.size(level_name)[0]
        
        # Create the text surface with yellow color and outline
        color = pygame.Color(255, 255, 0)
        text_surface = self.render_text_outlined(level_name, color)
        
        # Position the text at the bottom center of the screen
        rect = pygame.Rect(
            (self.screen.get_width() - text_width) // 2,
            self.screen.get_height() - 50,
            text_surface.get_width(),
            text_surface.get_height()
        )
        
        # Draw the text
        self.screen.blit(text_surface, rect)
    
    def render_text_outlined(self, text: str, color: pygame.Color) -> pygame.Surface:
        """
        Render text with outline.
        
        Args:
            text: The text to render
            color: The text color
            
        Returns:
            pygame.Surface: The rendered text surface
        """
        # Render text with black outline
        black = pygame.Color(0, 0, 0)
        
        # First render the text in the main color
        text_surface = self.font.render(text, True, color)
        
        # Create a larger surface for the outlined text
        outline_surface = pygame.Surface(
            (text_surface.get_width() + 2, text_surface.get_height() + 2),
            pygame.SRCALPHA
        )
        
        # Blit the text at various positions to create outline
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:  # Skip the center
                    outline_text = self.font.render(text, True, black)
                    outline_surface.blit(outline_text, (dx + 1, dy + 1))
        
        # Now blit the main text in the center
        outline_surface.blit(text_surface, (1, 1))
        
        return outline_surface
    
    def draw_edge(self, start, end) -> None:
        """
        Draw edge between two nodes.
        
        Args:
            start: The start node
            end: The end node
        """
        if not self.screen:
            return
            
        # Get coordinates
        x1 = int(start.get_loc().get_x())
        y1 = int(start.get_loc().get_y())
        x2 = int(end.get_loc().get_x())
        y2 = int(end.get_loc().get_y())
        
        # Color in RGBA format (same as 0xffff00ff in C++)
        color = (255, 255, 0, 255)
        
        # Draw anti-aliased lines
        pygame.gfxdraw.line(self.screen, x1, y1, x2, y2, color)
        pygame.gfxdraw.line(self.screen, x1 - 1, y1 - 1, x2 - 1, y2 - 1, color)
        pygame.gfxdraw.line(self.screen, x1 + 1, y1 + 1, x2 + 1, y2 + 1, color)
        pygame.gfxdraw.line(self.screen, x1 - 1, y1 + 1, x2 - 1, y2 + 1, color)
        pygame.gfxdraw.line(self.screen, x1 + 1, y1 - 1, x2 + 1, y2 - 1, color)
