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

from gengine.no_copy import NoCopy
from gengine.agent.base_listener import BaseListener
from gengine.ex_info import ExInfo
from gengine.exceptions import LogicException, NameException
from gengine.log import log_debug

class BaseAgent(NoCopy, BaseListener):
    """
    Base class for all agents in the game engine.
    Agents are autonomous components that provide specific functionality.
    """
    
    # Class attribute to store the name constant (set by the agent_class decorator)
    _name_constant = None
    
    def __init__(self):
        """
        Initialize a new agent.
        """
        self.initialized = False
        
    def get_name(self):
        """
        Get the name of this agent.
        Uses the _name_constant class attribute set by the agent_class decorator.
        
        Returns:
            str: The name of the agent
        """
        if hasattr(self.__class__, '_name_constant') and self.__class__._name_constant is not None:
            return self.__class__._name_constant
        raise NotImplementedError("Agent class must use @agent_class decorator or override get_name()")
    
    def is_initialized(self):
        """
        Check if this agent has been initialized.
        
        Returns:
            bool: True if the agent has been initialized, False otherwise
        """
        return self.initialized
    
    def own_init(self):
        """
        Agent-specific initialization code.
        Override this method to provide custom initialization.
        """
        pass
    
    def own_update(self):
        """
        Agent-specific update code.
        Override this method to provide custom update logic.
        """
        pass
    
    def own_shutdown(self):
        """
        Agent-specific shutdown code.
        Override this method to provide custom shutdown logic.
        """
        pass
    
    def init(self):
        """
        Initialize this agent.
        """
        # NOTE: agent can call oneself in init()
        self.initialized = True
        self.own_init()
    
    def update(self):
        """
        Update this agent.
        
        Raises:
            LogicException: If the agent has not been initialized
        """
        if not self.initialized:
            raise LogicException(ExInfo("agent is not ready").add_info("name", self.get_name()))
        
        self.own_update()
    
    def shutdown(self):
        """
        Shut down this agent.
        """
        self.own_shutdown()
        self.initialized = False

# Decorator to define an agent class with a static agent() method
def agent_class(name_constant):
    """
    Decorator to define an agent class with a static agent() method.
    
    Args:
        name_constant (str): The name constant for this agent
        
    Returns:
        function: The decorator function
    """
    def decorator(cls):
        # Store the name constant as a class attribute
        cls._name_constant = name_constant
        
        # Define the static name method
        @staticmethod
        def s_name():
            return name_constant
        cls.s_name = s_name
        
        # Define the static agent method
        @staticmethod
        def agent():
            from gengine.agent.agent_pack import AgentPack
            result = AgentPack.get_agent(cls.s_name())
            if not isinstance(result, cls):
                raise NameException(ExInfo("cannot cast agent").add_info("name", cls.s_name()))
            return result
        cls.agent = agent

        if not hasattr(cls, "get_instance"):
            cls.get_instance = agent
        
        return cls
    return decorator
