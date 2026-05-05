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

import inspect
import sys

class Log:
    """
    Logging utility class.
    Provides methods for logging messages at different priority levels.
    """
    
    # Log priority levels, like syslog
    LEVEL_DEBUG = 7
    LEVEL_INFO = 6
    LEVEL_WARNING = 4
    LEVEL_ERROR = 3
    
    # Default log level
    _log_level = LEVEL_INFO
    
    @classmethod
    def set_log_level(cls, log_level):
        """
        Set the current log level.
        
        Args:
            log_level (int): The new log level
        """
        cls._log_level = log_level
    
    @classmethod
    def get_log_level(cls):
        """
        Get the current log level.
        
        Returns:
            int: The current log level
        """
        return cls._log_level
    
    @classmethod
    def log(cls, level, file, line, info):
        """
        Log a message if its priority level is less than or equal to the current log level.
        
        Args:
            level (int): The priority level of the message
            file (str): The source file name
            line (int): The line number in the source file
            info (ExInfo or str): The detailed information to log
        """
        if level <= cls._log_level:
            level_name = "UNKNOWN"
            
            if level == cls.LEVEL_DEBUG:
                level_name = "DEBUG"
            elif level == cls.LEVEL_INFO:
                level_name = "INFO"
            elif level == cls.LEVEL_WARNING:
                level_name = "WARNING"
            elif level == cls.LEVEL_ERROR:
                level_name = "ERROR"
            
            # Handle different info types
            message = ""
            if hasattr(info, "what") and callable(info.what):
                message = info.what()
            elif isinstance(info, str):
                message = info
            else:
                message = str(info)
            
            print(f"{file}:{line}: {level_name} {message}", file=sys.stderr)

def log_debug(info):
    """
    Log a debug message.
    
    Args:
        info (ExInfo or str): The detailed information to log
    """
    frame = inspect.currentframe().f_back
    Log.log(Log.LEVEL_DEBUG, frame.f_code.co_filename, frame.f_lineno, info)

def log_info(info):
    """
    Log an info message.
    
    Args:
        info (ExInfo or str): The detailed information to log
    """
    frame = inspect.currentframe().f_back
    Log.log(Log.LEVEL_INFO, frame.f_code.co_filename, frame.f_lineno, info)

def log_warning(info):
    """
    Log a warning message.
    
    Args:
        info (ExInfo or str): The detailed information to log
    """
    frame = inspect.currentframe().f_back
    Log.log(Log.LEVEL_WARNING, frame.f_code.co_filename, frame.f_lineno, info)

def log_error(info):
    """
    Log an error message.
    
    Args:
        info (ExInfo or str): The detailed information to log
    """
    frame = inspect.currentframe().f_back
    Log.log(Log.LEVEL_ERROR, frame.f_code.co_filename, frame.f_lineno, info)