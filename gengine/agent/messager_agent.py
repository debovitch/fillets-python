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

from gengine.agent.base_agent import BaseAgent, agent_class
from gengine.name import Name
from gengine.log import log_debug
from gengine.ex_info import ExInfo
from gengine.exceptions import NameException

@agent_class(Name.MESSAGER_NAME)
class MessagerAgent(BaseAgent):
    """
    Agent that manages the message passing system.
    Keeps track of all listeners and forwards messages to them.
    """
    
    def __init__(self):
        """
        Initialize the messager agent.
        """
        super().__init__()
        self.listeners = {}
        
    def get_name(self):
        """
        Get the name of this agent.
        
        Returns:
            str: The name of the agent
        """
        return Name.MESSAGER_NAME
    
    def add_listener(self, listener):
        """
        Register a listener to receive messages.
        
        Args:
            listener (BaseListener): The listener to register
        """
        self.listeners[listener.get_name()] = listener
    
    def remove_listener(self, listener_name):
        """
        Unregister a listener so it no longer receives messages.
        
        Args:
            listener_name (str): The name of the listener to unregister
        """
        if listener_name in self.listeners:
            del self.listeners[listener_name]
    
    def forward_new_msg(self, msg):
        """
        Forward a message to its intended recipient.
        
        Args:
            msg (BaseMsg): The message to forward
            
        Raises:
            NameException: If the recipient cannot be found
        """
        listener_name = msg.get_listener_name()
        # log_debug(ExInfo("received new message").add_info("msg", msg.to_string()))
        
        if listener_name not in self.listeners:
            raise NameException(ExInfo("cannot find listener").add_info("name", listener_name))
        
        msg.send_actual(self.listeners[listener_name])