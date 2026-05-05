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
from gengine.no_copy import NoCopy
from gengine.key_stroke import KeyStroke
from gengine.log import log_debug, log_warning
from gengine.ex_info import ExInfo
from gengine.exceptions import LogicException

class KeyBinder(NoCopy):
    """
    Key binder for mapping keystrokes to messages.
    """
    
    def __init__(self):
        """
        Initialize a new key binder.
        """
        self.strokes = {}  # Maps KeyStroke to BaseMsg
    
    def __del__(self):
        """
        Clean up when the key binder is deleted.
        """
        # The messages will be cleaned up by Python's garbage collection
        pass
    
    def add_stroke(self, stroke, msg):
        """
        Bind a keystroke to a message.
        
        Args:
            stroke (KeyStroke): The keystroke
            msg (BaseMsg): The message to raise (will be cloned)
            
        Raises:
            LogicException: If the keystroke is already occupied
        """
        if stroke in self.strokes:
            raise LogicException(ExInfo("keystroke is occupied").add_info("keystroke", stroke.to_string()))
        
        self.strokes[stroke] = msg
        log_debug(ExInfo("binding keystroke")
                 .add_info("keystroke", stroke.to_string())
                 .add_info("msg", msg.to_string()))
    
    def remove_stroke(self, stroke):
        """
        Remove a keystroke binding.
        
        Args:
            stroke (KeyStroke): The keystroke to remove
        """
        if stroke in self.strokes:
            del self.strokes[stroke]
        else:
            log_warning(ExInfo("keystroke does not exist").add_info("keystroke", stroke.to_string()))
    
    def key_down(self, event):
        """
        Handle a keydown event, find the keystroke and send the message.
        
        Args:
            event (pygame.event.Event): The key event
        """
        stroke = KeyStroke(event)
        if stroke in self.strokes:
            self.strokes[stroke].send_clone()