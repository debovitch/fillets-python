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
from typing import Optional
from gengine.resource.resource_pack import ResourcePack
from gengine.resource.res_cache import ResCache
from gengine.ex_info import ExInfo
from gengine.log import log_debug
from gengine.agent.option_agent import OptionAgent
from gengine.exceptions import ResourceException

class ResImagePack(ResourcePack[pygame.Surface]):
    """
    Image resources and image loading.
    Manages loading, caching, and unloading of image resources.
    """
    
    # Shared cache for all image packs
    # The cache holds up to 265 images, which is enough to contain all fish images
    # and animations from the 'barrel' level.
    CACHE: Optional[ResCache] = None
    
    def __init__(self, caching_enabled: bool = True):
        """
        Initialize a new image pack.
        
        Args:
            caching_enabled: Whether to use the image cache
        """
        super().__init__()
        self.caching_enabled = False
        
        if caching_enabled:
            # Initialize the cache if it doesn't exist yet
            if ResImagePack.CACHE is None:
                ResImagePack.CACHE = ResCache(265, ResImagePack(False))
            
            # Check if caching is enabled in options
            self.caching_enabled = OptionAgent.agent().get_as_bool("cache_images", True)
    
    def get_name(self) -> str:
        """
        Get the name of this resource pack.
        
        Returns:
            str: The name of the resource pack
        """
        return "image_pack"
    
    @staticmethod
    def load_image(file_path) -> pygame.Surface:
        """
        Load unshared image from file and convert image to display format.
        
        Args:
            file_path: The path to the image file
            
        Returns:
            pygame.Surface: The loaded image
            
        Raises:
            ResourceException: If the image cannot be loaded or converted
        """
        # Get the path as a string
        path_str = file_path
        if hasattr(file_path, 'get_native'):
            path_str = file_path.get_native()
        
        try:
            # Load the image
            image = pygame.image.load(path_str)
            
            # Convert to display format with alpha
            surface = image.convert_alpha()
            
            return surface
        except pygame.error as e:
            raise ResourceException(ExInfo("Failed to load image")
                                  .add_info("file", path_str)
                                  .add_info("error", str(e)))
    
    def add_image(self, name: str, file_path) -> None:
        """
        Store image from file.
        
        Args:
            name: The name to store the image under
            file_path: The path to the image file
            
        Raises:
            ResourceException: If the image cannot be loaded or converted
        """
        surface = None
        
        # Use the cache if enabled
        if self.caching_enabled and ResImagePack.CACHE is not None:
            # Get the path as a string for cache lookups
            path_str = file_path
            if hasattr(file_path, 'get_posix_name'):
                path_str = file_path.get_posix_name()
            
            # Check the cache first
            surface = ResImagePack.CACHE.get(path_str)
            if not surface:
                # Load and cache the image
                surface = self.load_image(file_path)
                ResImagePack.CACHE.put(path_str, surface)
        else:
            # Load the image directly
            surface = self.load_image(file_path)
        
        # Store the image
        self.add_res(name, surface)
        
    def get_image(self, name: str) -> pygame.Surface:
        """
        Get an image by name.
        
        Args:
            name: The name of the image
            
        Returns:
            pygame.Surface: The image surface or None if not found
        """
        return self.find_res(name)
    
    def add_image_surface(self, name: str, surface: pygame.Surface) -> None:
        """
        Store an already-created surface directly.
        
        Args:
            name: The name to store the image under
            surface: The pygame Surface to store
        """
        # Store the image
        self.add_res(name, surface)
    
    def unload_res(self, res: pygame.Surface) -> None:
        """
        Free the given resource.
        
        Args:
            res: The resource to free
        """
        if self.caching_enabled and ResImagePack.CACHE is not None:
            # Let the cache handle the resource lifetime
            ResImagePack.CACHE.release(res)
        else:
            # In Python/Pygame, we don't need to explicitly free surfaces
            # They will be garbage collected
            pass