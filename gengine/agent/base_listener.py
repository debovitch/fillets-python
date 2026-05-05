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

from gengine.i_named import INamed
from gengine.exceptions import UnknownMsgException

class BaseListener(INamed):
    """
    Base class for all message listeners.
    Listeners must register themselves with the MessagerAgent to receive messages.
    """
    
    def register_watcher(self, param):
        """
        Register self as a watcher for a parameter.
        A string message param_changed(param) will be sent when the parameter changes.
        
        Args:
            param (str): The parameter to watch
        """
        # Import here to avoid circular imports
        from gengine.agent.option_agent import OptionAgent
        from gengine.message.string_msg import StringMsg
        
        event = StringMsg(self, "param_changed", param)
        OptionAgent.agent().add_watcher(param, event)
    
    def remove_watchers(self):
        """
        Remove all watchers registered by this listener.
        """
        # Import here to avoid circular imports
        from gengine.agent.option_agent import OptionAgent
        
        OptionAgent.agent().remove_watchers(self.get_name())
    
    def receive_simple(self, msg):
        """
        Handle a simple message.
        
        Args:
            msg (SimpleMsg): The message to handle
            
        Raises:
            UnknownMsgException: If the message cannot be handled
        """
        raise UnknownMsgException(msg)
    
    def receive_int(self, msg):
        """
        Handle an integer message.
        
        Args:
            msg (IntMsg): The message to handle
            
        Raises:
            UnknownMsgException: If the message cannot be handled
        """
        raise UnknownMsgException(msg)
    
    def receive_string(self, msg):
        """
        Handle a string message.
        
        Args:
            msg (StringMsg): The message to handle
            
        Raises:
            UnknownMsgException: If the message cannot be handled
        """
        raise UnknownMsgException(msg)