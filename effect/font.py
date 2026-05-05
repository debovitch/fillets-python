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
TrueType UTF-8 font class.
Translated from Font.h and Font.cpp
"""

import pygame
from gengine.path import Path
from gengine.no_copy import NoCopy
from gengine.log import log_warning
from gengine.ex_info import ExInfo

class Font(NoCopy):
    """
    TrueType UTF-8 font wrapper.
    Manages font loading and rendering.
    """
    
    @staticmethod
    def init():
        """
        Initialize font rendering subsystem.
        """
        pygame.font.init()
    
    @staticmethod
    def shutdown():
        """
        Shut down font rendering subsystem.
        """
        pygame.font.quit()
    
    @staticmethod
    def biditize(text):
        """
        Process bidirectional text.
        
        Args:
            text: The text to process
            
        Returns:
            str: The processed text
        """
        # Note: fribidi not implemented in this version
        return text
    
    def __init__(self, file_ttf, height):
        """
        Create a new font from file.
        
        Args:
            file_ttf: Path to TTF file
            height: Font height
        """
        NoCopy.__init__(self)
        
        # Load the font
        try:
            path = file_ttf.get_native()
            self.ttfont = pygame.font.Font(path, height)
        except Exception as e:
            from gengine.exceptions import TTFException
            raise TTFException(ExInfo("OpenFont").add_info("file", path))
        
        # Set background color (transparent)
        self.bg = (10, 10, 10, 0)
    
    def get_height(self):
        """
        Get the font height.
        
        Returns:
            int: The font height in pixels
        """
        return self.ttfont.get_height()
    
    def calc_text_width(self, text):
        """
        Calculate the width of text in this font.
        
        Args:
            text: The text to measure
            
        Returns:
            int: The text width in pixels
        """
        return self.ttfont.size(text)[0]
    
    def render_text(self, text, color):
        """
        Render text with the specified color.
        
        Args:
            text: UTF-8 encoded text
            color: Text color (RGBA tuple)
            
        Returns:
            pygame.Surface: The rendered text surface
        """
        content = self.biditize(text)
        
        # Handle empty text
        if not text:
            content = " "
            log_warning(ExInfo("empty text to render")
                     .add_info("r", color[0])
                     .add_info("g", color[1])
                     .add_info("b", color[2]))
        
        # Render the text with antialiasing
        surface = self.ttfont.render(content, True, color)
        
        return surface
    
    def render_text_outlined(self, text, color, outline_width=1):
        """
        Render text with a black outline.
        
        Args:
            text: UTF-8 encoded text
            color: Text color (RGBA tuple)
            outline_width: Width of the outline
            
        Returns:
            pygame.Surface: The rendered text surface with outline
        """
        BLACK = (0, 0, 0, 255)
        
        # Add spaces to ensure space for outline
        padded_text = " " + text + " "
        
        # Create the text surface
        text_surface = self.render_text(padded_text, color)
        
        # Create a larger surface for the outlined text
        width, height = text_surface.get_size()
        outline_surface = pygame.Surface(
            (width + outline_width*2, height + outline_width*2),
            pygame.SRCALPHA
        )
        
        # Draw outline by offsetting the text in different directions
        for dx in range(-outline_width, outline_width+1):
            for dy in range(-outline_width, outline_width+1):
                if dx != 0 or dy != 0:  # Skip the center
                    outline_surface.blit(
                        self.render_text(padded_text, BLACK),
                        (outline_width + dx, outline_width + dy)
                    )
        
        # Draw the text on top
        outline_surface.blit(text_surface, (outline_width, outline_width))
        
        return outline_surface