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

from abc import ABC, abstractmethod

class BaseMsg(ABC):
    """
    Base class for all messages in the messaging system.
    """
    
    def __init__(self, listener_name, name, listener=None):
        """
        Initialize a new message.
        
        Args:
            listener_name (str): The name of the destination listener
            name (str): The name of the message
        """
        self.listener_name = listener_name
        self.name = name
        self.listener = listener
    
    @abstractmethod
    def clone(self):
        """
        Create a copy of this message.
        
        Returns:
            BaseMsg: A copy of this message
        """
        pass
    
    @abstractmethod
    def send_actual(self, listener):
        """
        Send this message to the specified listener.
        
        Args:
            listener: The listener to send the message to
        """
        pass
    
    def send_clone(self):
        """
        Send a copy of this message to its designated recipient.
        """
        self.clone().send()

    def send(self):
        """
        Send this message to its designated recipient.
        """
        if self.listener is not None:
            self.send_actual(self.listener)
            return

        # Import here to avoid circular import
        from gengine.agent.messager_agent import MessagerAgent
        MessagerAgent.agent().forward_new_msg(self)
    
    def equals_name(self, name):
        """
        Check if this message has the specified name.
        
        Args:
            name (str): The name to check against
            
        Returns:
            bool: True if the message has the specified name, False otherwise
        """
        return self.name == name
    
    def get_msg_name(self):
        """
        Get the name of this message.
        
        Returns:
            str: The name of the message
        """
        return self.name
    
    def get_listener_name(self):
        """
        Get the name of the listener this message is intended for.
        
        Returns:
            str: The name of the listener
        """
        return self.listener_name
    
    def to_string(self):
        """
        Get a string representation of this message.
        
        Returns:
            str: A string representation of the message
        """
        return f"{self.listener_name}->{self.name}"
