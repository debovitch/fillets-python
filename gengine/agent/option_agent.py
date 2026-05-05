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
import locale
from gengine.agent.base_agent import BaseAgent, agent_class
from gengine.name import Name
from gengine.ex_info import ExInfo
from gengine.log import log_debug, Log
from gengine.exceptions import LogicException
from gengine.message.string_msg import StringMsg

@agent_class(Name.OPTION_NAME)
class OptionAgent(BaseAgent):
    """
    Agent that manages game options and configuration.
    """
    
    # Define parameter types
    PARAM_TYPE_BOOLEAN = "boolean"
    PARAM_TYPE_NUMBER = "number"
    PARAM_TYPE_STRING = "string"
    PARAM_TYPE_PATH = "path"
    
    # Configuration file path
    CONFIG_FILE = "script/options.lua"
    
    # Default user data directory
    USER_DATA_DIR = ".fillets-python"
    
    # System data directory - will be set by build system
    SYSTEM_DATA_DIR = ""
    
    def __init__(self):
        """
        Initialize the option agent.
        """
        super().__init__()
        self.params = {}
        self.defaults = {}
        self.watchers = {}  # Dictionary mapping parameter names to lists of messages
        self.param_descriptions = {}  # Dictionary mapping parameter names to their descriptions
        
    def get_name(self):
        """
        Get the name of this agent.
        
        Returns:
            str: The name of the agent
        """
        return Name.OPTION_NAME
    
    def own_init(self):
        """
        Initialize options and configuration.
        """
        self.prepare_version()
        self.prepare_data_paths()
        self.prepare_lang()
        
        # Read configuration files
        self.read_system_config()
        self.read_user_config()
    
    def own_shutdown(self):
        """
        Clean up when shutting down.
        """
        pass
    
    def prepare_version(self):
        """
        Set version information.
        """
        # TODO: This would be set from build system, for now use placeholder version
        self.set_param("version", "1.0.0")
        self.set_param("codename", "Python")
    
    def prepare_data_paths(self):
        """
        Set up the data paths for the game.
        """
        # Set user data directory
        home_dir = os.path.expanduser("~")
        user_dir = os.path.join(home_dir, self.USER_DATA_DIR)
        self.set_param("userdir", user_dir)
        
        # Set system data directory. The C++ version receives this from the
        # build/install system; in the source tree the data directory lives
        # next to python_version.
        repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        source_data_dir = os.path.join(repo_root, "data")
        self.set_param("systemdir", source_data_dir if os.path.isdir(source_data_dir) else "data")
        
        # Create user directory if it doesn't exist
        if not os.path.exists(user_dir):
            try:
                os.makedirs(user_dir)
            except OSError:
                log_debug(ExInfo("cannot create user directory").add_info("dir", user_dir))
    
    def prepare_lang(self):
        """
        Set up language and locale settings.
        """
        # Set default language to English
        self.set_default("lang", "en")
        
        # Try to detect system language
        try:
            system_lang = locale.getdefaultlocale()[0]
            if system_lang:
                lang_code = system_lang.split('_')[0]
                self.set_param("lang", lang_code)
        except (IndexError, ValueError):
            pass
        
        # Set locale for messages
        locale.setlocale(locale.LC_MESSAGES, '')
    
    def parse_cmd_opt(self, args):
        """
        Parse command line options.
        
        Args:
            args (list): Command line arguments
        """
        # Skip the program name
        args = args[1:]
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg.startswith("--"):
                # Long option
                self.parse_dash_opt(arg)
            elif arg.startswith("-"):
                # Short option
                self.parse_dash_opt(arg)
            else:
                # Parameter option (name=value)
                self.parse_param_opt(arg)
            
            i += 1
    
    def parse_dash_opt(self, arg):
        """
        Parse a dash option (--option or -o).
        
        Args:
            arg (str): The option to parse
        """
        if arg.startswith("--"):
            # Long option: --option or --option=value
            option = arg[2:]  # Remove leading --
            if "=" in option:
                name, value = option.split("=", 1)
                self.set_param(name, value)
            else:
                # Boolean option
                self.set_param(option, "true")
        elif arg.startswith("-"):
            # Short option: -o
            option = arg[1:]  # Remove leading -
            # For now, just set it as a boolean flag
            self.set_param(option, "true")
    
    def parse_param_opt(self, arg):
        """
        Parse a parameter option (name=value).
        
        Args:
            arg (str): The option to parse
        """
        name, value = self.split_opt(arg)
        if name and value:
            self.set_param(name, value)
    
    def split_opt(self, option):
        """
        Split an option string into name and value.
        
        Args:
            option (str): The option string in format "name=value"
            
        Returns:
            tuple: A tuple (name, value) or (None, None) if the format is invalid
        """
        parts = option.split('=', 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return None, None
    
    def read_system_config(self):
        """
        Read the system configuration file.
        """
        # TODO: Implement reading from system config
        pass
    
    def read_user_config(self):
        """
        Read the user configuration file.
        """
        # TODO: Implement reading from user config
        pass
    
    def set_param(self, name, value):
        """
        Set a parameter value.
        
        Args:
            name (str): The parameter name
            value: The parameter value (will be converted to string)
        """
        old_value = self.params.get(name)
        new_value = str(value)
        
        if old_value != new_value:
            self.params[name] = new_value
            # log_debug(f"Parameter '{name}' set to '{new_value}'")
            self.notify_watchers(name)
    
    def set_persistent(self, name, value):
        """
        Set a parameter value and save it to the user configuration.
        
        Args:
            name (str): The parameter name
            value: The parameter value (will be converted to string)
        """
        self.set_param(name, value)
        # TODO: Implement saving to user config
    
    def set_default(self, name, value):
        """
        Set a default value for a parameter.
        
        Args:
            name (str): The parameter name
            value: The default value (will be converted to string)
        """
        self.defaults[name] = str(value)
        # log_debug(f"Default for parameter '{name}' set to '{value}'")
        
    def add_param(self, name, param_type, description):
        """
        Add a parameter with type and description.
        
        Args:
            name (str): Parameter name
            param_type (str): Parameter type (boolean, number, string, path)
            description (str): Parameter description
        """
        self.param_descriptions[name] = (param_type, description)
    
    def get_param(self, name, implicit=""):
        """
        Get a parameter value.
        
        Args:
            name (str): The parameter name
            implicit (str): The default value if the parameter is not set
            
        Returns:
            str: The parameter value or the implicit value if not set
        """
        if name in self.params:
            return self.params[name]
        if name in self.defaults:
            return self.defaults[name]
        return implicit
    
    def get_as_int(self, name, implicit=0):
        """
        Get a parameter value as an integer.
        
        Args:
            name (str): The parameter name
            implicit (int): The default value if the parameter is not set or not an integer
            
        Returns:
            int: The parameter value or the implicit value if not set
        """
        try:
            return int(self.get_param(name, str(implicit)))
        except ValueError:
            return implicit
    
    def get_as_bool(self, name, implicit=False):
        """
        Get a parameter value as a boolean.
        
        Args:
            name (str): The parameter name
            implicit (bool): The default value if the parameter is not set
            
        Returns:
            bool: The parameter value or the implicit value if not set
        """
        value = self.get_param(name, "").lower()
        if value in ("1", "true", "yes", "on"):
            return True
        if value in ("0", "false", "no", "off"):
            return False
        return implicit
    
    def add_watcher(self, name, msg):
        """
        Add a watcher for a parameter.
        The watcher will be notified when the parameter changes.
        
        Args:
            name (str): The parameter name to watch
            msg (BaseMsg): The message to send when the parameter changes
        """
        if name not in self.watchers:
            self.watchers[name] = []
        self.watchers[name].append(msg)
    
    def remove_watchers(self, listener_name):
        """
        Remove all watchers for a listener.
        
        Args:
            listener_name (str): The name of the listener
        """
        for name in list(self.watchers.keys()):
            self.watchers[name] = [msg for msg in self.watchers[name] 
                                if msg.get_listener_name() != listener_name]
            if not self.watchers[name]:
                del self.watchers[name]
    
    def notify_watchers(self, name):
        """
        Notify watchers that a parameter has changed.
        
        Args:
            name (str): The name of the parameter that changed
        """
        if name in self.watchers:
            for msg in self.watchers[name]:
                msg.send_clone()
    
    def receive_string(self, msg):
        """
        Handle string messages.
        
        Args:
            msg (StringMsg): The message to handle
            
        Raises:
            UnknownMsgException: If the message cannot be handled
        """
        if msg.equals_name("param_changed"):
            # This is our own message, no need to handle it
            return
        
        # Use the parent class implementation
        super().receive_string(msg)
