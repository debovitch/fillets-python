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

from typing import TypeVar, Generic, List, Optional, Dict, Any
from gengine.no_copy import NoCopy
from gengine.log import log_debug, log_warning
from gengine.ex_info import ExInfo

# Generic type for resources
T = TypeVar('T')

class CacheEntry(Generic[T]):
    """
    Entry in the resource cache.
    """
    
    def __init__(self):
        """
        Initialize a new cache entry.
        """
        self.name = ""
        self.value = None
        self.refcount = 0

class ResCache(NoCopy, Generic[T]):
    """
    A fixed size cache for any resources.
    Uses a reference counting system to manage resource lifetimes.
    """
    
    def __init__(self, capacity: int, unloader: Any):
        """
        Create a cache with the given capacity.
        The given unloader must have disabled caching to prevent an infinite loop.
        
        Args:
            capacity: The maximum number of resources to cache
            unloader: The resource pack to use for unloading resources
        """
        self.entries: List[CacheEntry[T]] = [CacheEntry() for _ in range(capacity)]
        self.next_pos = 0
        self.unloader = unloader
    
    def __del__(self):
        """
        Clean up resources when the cache is deleted.
        """
        # The resources will be cleaned up by the unloader
        pass
    
    def get(self, name: str) -> Optional[T]:
        """
        Returns a found value or None.
        The returned item should be released via release().
        
        Args:
            name: The name of the resource to get
            
        Returns:
            The resource or None if not found
        """
        entry = self.get_entry(name)
        if not entry:
            return None
        
        entry.refcount += 1
        return entry.value
    
    def put(self, name: str, value: T) -> None:
        """
        Notes a new value.
        The caller should release it later via release().
        
        Args:
            name: The name to store the resource under
            value: The resource to store
        """
        entry = self.find_next_unused_entry()
        if not entry:
            log_debug(ExInfo("cannot fit into cache").add_info("name", name))
            return
        
        if entry.value is not None:
            self.unloader.unload_res(entry.value)
        
        entry.name = name
        entry.value = value
        entry.refcount = 1
    
    def release(self, value: T) -> None:
        """
        Releases or takes responsibility for the given value.
        
        Args:
            value: The resource to release
        """
        found = self.get_by_value(value)
        if found:
            found.refcount -= 1
            if found.refcount < 0:
                log_warning(ExInfo("extra release of a cache entry"))
                found.refcount = 0
        else:
            self.unloader.unload_res(value)
    
    def get_entry(self, name: str) -> Optional[CacheEntry[T]]:
        """
        Returns the matching CacheEntry or None.
        
        Args:
            name: The name of the resource
            
        Returns:
            The cache entry or None if not found
        """
        for entry in self.entries:
            if entry.value is not None and entry.name == name:
                return entry
        
        return None
    
    def get_by_value(self, value: T) -> Optional[CacheEntry[T]]:
        """
        Returns the matching CacheEntry or None.
        
        Args:
            value: The resource value
            
        Returns:
            The cache entry or None if not found
        """
        for entry in self.entries:
            if entry.value == value:
                return entry
        
        return None
    
    def find_next_unused_entry(self) -> Optional[CacheEntry[T]]:
        """
        Returns a next unused CacheEntry or None when all entries are full.
        Uses a round-robin approach to find the next available entry.
        
        Returns:
            An unused cache entry or None if all are in use
        """
        for _ in range(len(self.entries)):
            entry = self.entries[self.next_pos]
            self.next_pos = (self.next_pos + 1) % len(self.entries)
            
            if entry.refcount <= 0:
                return entry
        
        return None