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

import os
import sys
from gengine.ex_info import ExInfo
from gengine.log import log_info

class Path:
    """
    Path to installed game data.
    Handles system and user data paths.
    """
    
    @staticmethod
    def check_exists(path_obj):
        """
        Static method to check if a path exists.
        
        Args:
            path_obj: The path to check (can be a Path object or a string)
            
        Returns:
            bool: True if the path exists, False otherwise
        """
        if hasattr(path_obj, 'get_native'):
            # It's a Path object
            path_str = path_obj.get_native()
        else:
            # It's a string
            path_str = str(path_obj)
            
        if not path_str:
            return False
            
        try:
            return os.path.exists(path_str)
        except Exception as e:
            from gengine.log import log_warning
            log_warning(f"Error checking if path exists: {path_str}, error: {str(e)}")
            return False
    
    def __init__(self, file_path):
        """
        Initialize a new path.
        
        Args:
            file_path (str): The path to the file
        """
        self.path = file_path
    
    @staticmethod
    def data_read_path(file):
        """
        Get a path for reading data, checking user path first, then system path.
        
        Args:
            file (str): The file to get the path for
            
        Returns:
            Path: The path to the file
        """
        # Special case for menu placeholder images
        if file.startswith("images/menu/dot_"):
            # Look for placeholder images in our local data directory first
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            local_path = os.path.join(current_dir, "data", file)
            
            if os.path.exists(local_path):
                return Path(local_path)
        
        try:
            data_path = Path.data_path(file, False)
            if data_path.exists():
                return data_path
        except Exception as e:
            pass

        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Try direct data folder in the source tree.
        direct_path = os.path.join(current_dir, "data", file)
        if os.path.exists(direct_path):
            return Path(direct_path)

        # Try extracted fillets-ng-data folder.
        data_path = os.path.join(current_dir, "fillets-ng-data-1.0.1", file)
        if os.path.exists(data_path):
            return Path(data_path)

        # Return the best diagnostic path even when the file does not exist.
        return Path(os.path.join(current_dir, "data", file))
    
    @staticmethod
    def data_write_path(file):
        """
        Get a path for writing data, always in the user data directory.
        
        Args:
            file (str): The file to get the path for
            
        Returns:
            Path: The path to the file
        """
        try:
            return Path.data_path(file, True)
        except Exception as e:
            # For testing, provide a fallback
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            return Path(os.path.join(output_dir, file))
    
    @staticmethod
    def data_system_path(file):
        """
        Get a path in the system data directory.
        
        Args:
            file (str): The file to get the path for
            
        Returns:
            Path: The path to the file
        """
        # Import here to avoid circular imports
        from gengine.agent.option_agent import OptionAgent
        
        system_dir = OptionAgent.agent().get_param("systemdir")
        return Path.construct_path(system_dir, file)
    
    @staticmethod
    def data_user_path(file):
        """
        Get a path in the user data directory.
        
        Args:
            file (str): The file to get the path for
            
        Returns:
            Path: The path to the file
        """
        # Import here to avoid circular imports
        from gengine.agent.option_agent import OptionAgent
        
        user_dir = OptionAgent.agent().get_param("userdir")
        return Path.construct_path(user_dir, file)
    
    @staticmethod
    def data_path(file, writeable):
        """
        Try to return a user data path, otherwise fall back to the system data path.
        
        Args:
            file (str): The file to get the path for
            writeable (bool): Whether we want to write to the file
            
        Returns:
            Path: The path to the file
        """
        data_path = Path.data_user_path(file)
        
        if not data_path.exists():
            if writeable:
                # Create the directory if it doesn't exist
                dir_path = os.path.dirname(data_path.get_native())
                if not os.path.exists(dir_path):
                    try:
                        log_info(ExInfo("creating path").add_info("path", dir_path))
                        os.makedirs(dir_path, exist_ok=True)
                    except OSError as e:
                        log_info(ExInfo("cannot create path").add_info("path", dir_path).add_info("error", str(e)))
            else:
                # Use the system path for reading
                data_path = Path.data_system_path(file)
        
        return data_path
    
    @staticmethod
    def localize_path(original):
        """
        Localize a path based on the current language.
        
        Args:
            original (str): The original path
            
        Returns:
            str: The localized path
        """
        # Import here to avoid circular imports
        from gengine.agent.option_agent import OptionAgent
        
        # If the path already exists, use it
        if os.path.exists(original):
            return original
        
        # Try to localize the path
        lang = OptionAgent.agent().get_param("lang")
        if lang and lang != "en":
            # Try with language-specific path
            path_parts = os.path.splitext(original)
            localized = f"{path_parts[0]}.{lang}{path_parts[1]}"
            if os.path.exists(localized):
                return localized
        
        return original
    
    @staticmethod
    def construct_path(directory, file):
        """
        Construct a path by joining a directory and a file.
        
        Args:
            directory (str): The directory
            file (str): The file
            
        Returns:
            Path: The constructed path
        """
        return Path(os.path.join(directory, file))
    
    def get_posix_name(self):
        """
        Get the path in POSIX format.
        
        Returns:
            str: The path in POSIX format
        """
        return self.path.replace("\\", "/")
    
    def get_native(self):
        """
        Get the path in native format.
        
        Returns:
            str: The path in native format
        """
        return self.path
    
    def exists(self):
        """
        Check if the path exists.
        
        Returns:
            bool: True if the path exists, False otherwise
        """
        if not self.path:
            return False
            
        try:
            return os.path.exists(self.path)
        except Exception as e:
            from gengine.log import log_warning
            log_warning(f"Error checking if path exists: {self.path}, error: {str(e)}")
            return False
