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
from gengine.i_named import INamed
from gengine.log import log_warning, log_debug
from gengine.ex_info import ExInfo
from gengine.random import Random
from typing import TypeVar, Generic, Dict, List, Optional, Any

# Generic type for resources
T = TypeVar('T')

class ResourcePack(INamed, Generic[T]):
    """
    Base class for resource management.
    Manages a collection of resources that can be accessed by name.
    """
    
    def __init__(self):
        """
        Initialize a new resource pack.
        """
        # Dictionary mapping resource names to lists of resources
        self.resources: Dict[str, List[T]] = {}
    
    @abstractmethod
    def unload_res(self, res: T) -> None:
        """
        Free the given resource.
        Must be implemented by derived classes.
        
        Args:
            res: The resource to free
        """
        pass
    
    def __del__(self):
        """
        Destructor to warn about unreleased resources.
        """
        try:
            if self.resources:
                from gengine.ex_info import ExInfo
                from gengine.log import log_warning
                
                # Create a basic info string without using to_string() which causes issues during shutdown
                res_info = "resources; name='" + self.get_name() + "'"
                
                # Add key names
                for key in self.resources.keys():
                    res_info += f"; key='{key}'"
                    
                log_warning(ExInfo("resources are not released").add_info("pack", res_info))
        except (ImportError, AttributeError):
            # During interpreter shutdown, modules might be gone already
            pass
    
    def remove_all(self) -> None:
        """
        Free all resources.
        """
        for _, resources in self.resources.items():
            for res in resources:
                self.unload_res(res)
        self.resources.clear()
    
    def remove_res(self, name: str) -> None:
        """
        Unload all resources with this name.
        
        Args:
            name: The name of the resources to remove
        """
        if name in self.resources:
            for res in self.resources[name]:
                self.unload_res(res)
            del self.resources[name]
            log_debug(ExInfo("removed resources").add_info("name", name))
    
    def add_res(self, name: str, res: T) -> None:
        """
        Store resource under this name.
        
        Args:
            name: The name to store the resource under
            res: The resource to store
        """
        if name not in self.resources:
            self.resources[name] = []
        self.resources[name].append(res)
    
    def get_res(self, name: str, rank: int = 0) -> T:
        """
        Get resource with this name at the specified rank.
        
        Args:
            name: The name of the resource
            rank: The index of the resource if multiple resources share the same name
            
        Returns:
            The requested resource
            
        Raises:
            ResourceException: If the resource does not exist
        """
        if name not in self.resources or rank >= len(self.resources[name]):
            from gengine.exceptions import ResourceException
            raise ResourceException(ExInfo("no such resource at index")
                                  .add_info("name", name)
                                  .add_info("index", rank)
                                  .add_info("pack", self.to_string()))
        
        return self.resources[name][rank]
    
    def get_range(self, name: str) -> List[T]:
        """
        Get all resources with this name.
        
        Args:
            name: The name of the resources
            
        Returns:
            A list of resources with the given name (can be empty)
        """
        if name in self.resources:
            return self.resources[name].copy()
        return []
    
    def get_random_res(self, name: str) -> Optional[T]:
        """
        Get resource at random index or return None.
        
        Args:
            name: The name of the resources
            
        Returns:
            A random resource with the given name or None if none exist
        """
        if name in self.resources and self.resources[name]:
            count = len(self.resources[name])
            return self.resources[name][Random.random_int(count)]
        else:
            log_warning(ExInfo("no such resource")
                       .add_info("name", name)
                       .add_info("pack", self.to_string()))
            return None
            
    def find_res(self, name: str) -> Optional[T]:
        """
        Find a resource by name, returning the first one or None if not found.
        
        Args:
            name: The name of the resource
            
        Returns:
            The first resource with the given name or None if none exist
        """
        if name in self.resources and self.resources[name]:
            return self.resources[name][0]
        return None
    
    def count_res(self, name: str) -> int:
        """
        Count resources with this name.
        
        Args:
            name: The name of the resources
            
        Returns:
            The number of resources with the given name
        """
        if name in self.resources:
            return len(self.resources[name])
        return 0
    
    def to_string(self) -> str:
        """
        Get a string representation of this resource pack.
        
        Returns:
            A string representation
        """
        available_res = ExInfo("resources").add_info("name", self.get_name())
        
        for key in self.resources.keys():
            available_res.add_info("key", key)
            
        return available_res.info()