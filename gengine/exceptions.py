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

class BaseException(Exception):
    """
    Base class for all game exceptions.
    """
    
    def __init__(self, ex_info):
        """
        Initialize with detailed exception information.
        
        Args:
            ex_info (ExInfo): Detailed exception information
        """
        self.ex_info = ex_info
        super().__init__(ex_info.what())
        
    def info(self):
        """
        Get the exception information.
        
        Returns:
            ExInfo: The exception information
        """
        return self.ex_info

class HelpException(BaseException):
    """
    Exception thrown when help is requested.
    """
    pass

class LogicException(BaseException):
    """
    Exception thrown when there's a logic error in the game.
    """
    pass

class NameException(BaseException):
    """
    Exception thrown when there's an issue with named objects.
    """
    pass

class ResourceException(BaseException):
    """
    Exception thrown when a resource cannot be found or loaded.
    """
    pass

class ScriptException(BaseException):
    """
    Exception thrown when a script cannot be executed.
    """
    pass

class UnknownMsgException(BaseException):
    """
    Exception thrown when a message cannot be handled.
    """
    def __init__(self, msg):
        """
        Initialize with the message that couldn't be handled.
        
        Args:
            msg: The message that couldn't be handled
        """
        from gengine.ex_info import ExInfo
        info = ExInfo("unknown message").add_info("msg", msg.to_string())
        super().__init__(info)