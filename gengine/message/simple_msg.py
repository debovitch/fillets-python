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

from gengine.message.base_msg import BaseMsg

class SimpleMsg(BaseMsg):
    """
    Simple text message without any additional data.
    """
    
    def __init__(self, listener_or_name, name):
        """
        Initialize a new simple message.
        
        Args:
            listener_or_name: Either a BaseListener object or the name of the listener
            name (str): The name of the message
        """
        listener = None

        # Check if listener_or_name is a BaseListener or a string
        if hasattr(listener_or_name, 'get_name'):
            listener_name = listener_or_name.get_name()
            listener = listener_or_name
        else:
            listener_name = listener_or_name
            
        super().__init__(listener_name, name, listener)
    
    def clone(self):
        """
        Create a copy of this message.
        
        Returns:
            SimpleMsg: A copy of this message
        """
        listener = self.listener if self.listener is not None else self.listener_name
        return SimpleMsg(listener, self.name)
    
    def send_actual(self, listener):
        """
        Send this message to the specified listener.
        
        Args:
            listener: The listener to send the message to
        """
        listener.receive_simple(self)
