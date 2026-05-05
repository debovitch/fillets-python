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
from gengine.ex_info import ExInfo
from gengine.exceptions import LogicException, NameException

class AgentPack(NoCopy):
    """
    Manages all agents in the game engine.
    Provides a singleton for accessing, initializing, updating, and shutting down agents.
    """
    
    # Singleton instance
    _singleton = None
    
    def __init__(self):
        """
        Initialize a new agent pack.
        
        Raises:
            LogicException: If an AgentPack already exists (it's a singleton)
        """
        if AgentPack._singleton is not None:
            raise LogicException(ExInfo("AgentPack is singleton"))
        
        AgentPack._singleton = self
        self.agents = {}
        
        # Initialize messager agent first
        from gengine.agent.messager_agent import MessagerAgent
        messager = MessagerAgent()
        messager.init()
        self.add_agent(messager)
    
    def __del__(self):
        """
        Clean up when the agent pack is deleted.
        """
        # The agents will be cleaned up by Python's garbage collection
        AgentPack._singleton = None
    
    def add_agent(self, agent):
        """
        Add an agent to the pack.
        Also adds the agent as a listener to the messager.
        
        Args:
            agent (BaseAgent): The agent to add
            
        Raises:
            NameException: If an agent with the same name already exists
        """
        agent_name = agent.get_name()
        
        if agent_name in self.agents:
            raise NameException(ExInfo("agent already exists").add_info("name", agent_name))
        
        self.agents[agent_name] = agent
        from gengine.agent.messager_agent import MessagerAgent
        MessagerAgent.agent().add_listener(agent)
    
    def remove_agent(self, name):
        """
        Remove an agent from the pack.
        Also removes the agent as a listener from the messager.
        
        Args:
            name (str): The name of the agent to remove
        """
        if name in self.agents:
            from gengine.agent.messager_agent import MessagerAgent
            MessagerAgent.agent().remove_listener(name)
            del self.agents[name]
    
    @staticmethod
    def get_agent(name):
        """
        Get an agent by name.
        
        Args:
            name (str): The name of the agent to get
            
        Returns:
            BaseAgent: The requested agent
            
        Raises:
            LogicException: If the AgentPack is not initialized
            NameException: If an agent with the given name does not exist
            LogicException: If the agent has not been initialized
        """
        if AgentPack._singleton is None:
            raise LogicException(ExInfo("AgentPack is not ready"))
        
        if name not in AgentPack._singleton.agents:
            raise NameException(ExInfo("cannot find agent").add_info("name", name))
        
        agent = AgentPack._singleton.agents[name]
        
        if not agent.is_initialized():
            raise LogicException(ExInfo("agent is not initialized").add_info("name", name))
        
        return agent
    
    def init(self, stop_agent=""):
        """
        Initialize all agents up to the specified stop agent.
        If stop_agent is not specified or not found, initializes all agents.
        
        Args:
            stop_agent (str): The name of the agent to stop at (not including this agent)
        """
        for name, agent in self.agents.items():
            if name == stop_agent:
                break
            
            if not agent.is_initialized():
                agent.init()
    
    def update(self):
        """
        Update all agents.
        """
        for agent in self.agents.values():
            agent.update()
    
    def shutdown(self):
        """
        Shut down all initialized agents in reverse order.
        """
        for name in reversed(list(self.agents.keys())):
            agent = self.agents[name]
            if agent.is_initialized():
                agent.shutdown()