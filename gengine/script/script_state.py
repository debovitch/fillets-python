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

"""
Script state for Lua integration.
"""

import lupa
from lupa import LuaRuntime
from gengine.no_copy import NoCopy
from gengine.path import Path
from gengine.log import log_debug, log_warning, log_error
from gengine.ex_info import ExInfo
from gengine.resource.script_exception import ScriptException

class ScriptState(NoCopy):
    """
    Independent Lua script state.
    Wraps the Lua runtime and provides methods to execute Lua code.
    """
    
    def __init__(self):
        """Initialize a new Lua script state."""
        NoCopy.__init__(self)
        
        # Create a Lua runtime
        self.state = LuaRuntime(unpack_returned_tuples=True)
        self.registry = {}  # Python-side registry for function references
        self.ref_counter = 0  # Counter for generating unique reference IDs
        
        # Set up standard Lua libraries
        # Note: Lupa already includes the standard libraries
        
        # Add traceback function for error handling
        self.prepare_error_handler()
    
    def prepare_error_handler(self):
        """Prepare error handler at global stack."""
        self.state.execute("""
            table.getn = table.getn or function(t) return #t end
            math.mod = math.mod or math.fmod
            loadstring = loadstring or load
            unpack = unpack or table.unpack
            _TRACEBACK = function(err)
                return debug.traceback(err, 2)
            end
        """)

    def _normalize_source(self, source):
        """Normalize legacy Lua source accepted by the original game runtime."""
        return source.replace("\\/", "/")
    
    def do_file(self, file_path):
        """
        Execute a Lua script file.
        
        Args:
            file_path (Path): Path to the script file
            
        Raises:
            ScriptException: If the script has an error
        """
        try:
            with open(file_path.get_native(), 'r', encoding='utf-8') as f:
                script = f.read()
            script = self._normalize_source(script)
            self.state.execute(script)
        except Exception as e:
            raise ScriptException(ExInfo("script failure")
                .add_info("error", str(e))
                .add_info("file", file_path.get_native()))
    
    def do_string(self, input_str):
        """
        Execute a Lua script string.
        
        Args:
            input_str (str): The Lua code to execute
            
        Raises:
            ScriptException: If the script has an error
        """
        try:
            input_str = self._normalize_source(input_str)
            self.state.execute(input_str)
        except Exception as e:
            raise ScriptException(ExInfo("script failure")
                .add_info("error", str(e))
                .add_info("script", input_str[:50] + "..." if len(input_str) > 50 else input_str))
    
    def register_function(self, name, func):
        """
        Register a Python function to be callable from Lua.
        
        Args:
            name (str): The function name in Lua
            func: The Python function to register
        """
        # Wrapper to handle Python exceptions
        def wrapped_func(*args):
            try:
                result = func(self, *args)
                return result
            except Exception as e:
                import traceback
                log_error(f"Error in Python function called from Lua: {type(e).__name__}: {e!r}\n{traceback.format_exc()}")
                raise
        
        # Register the function in the Lua global namespace
        self.state.globals()[name] = wrapped_func

    def register_func(self, name, func):
        """
        Register a Python function using the older translation API.

        Most callers expect Lua arguments directly. Some early ports kept the
        C++ convention of receiving a single args list; those functions are
        detected by an explicit ``args`` parameter name.
        """
        import inspect

        parameters = list(inspect.signature(func).parameters.values())
        wants_arg_list = len(parameters) == 1 and parameters[0].name in ("args", "argv")

        def wrapped_func(*args):
            try:
                if wants_arg_list:
                    return func(list(args))
                return func(*args)
            except Exception as e:
                import traceback
                log_error(f"Error in Python function called from Lua: {type(e).__name__}: {e!r}\n{traceback.format_exc()}")
                raise

        self.state.globals()[name] = wrapped_func
    
    def register_leader(self, leader):
        """
        Register a leader object for scripts to access.
        
        Args:
            leader: The leader object (usually a Scripter instance)
        """
        # Store the leader in registry for scripts to access
        self.state.globals()["_LEADER"] = leader
        self.registry["script_leader"] = leader

    def get_leader(self):
        """
        Get the registered script leader.

        Returns:
            object: The registered script leader
        """
        leader = self.state.globals()["_LEADER"]
        if leader is None:
            leader = self.registry.get("script_leader")
        return leader
    
    def call_command(self, func_ref, param):
        """
        Call a Lua function stored in the registry.
        
        Args:
            func_ref (int): Reference to the function
            param (int): Integer parameter to pass to the function
            
        Returns:
            bool: The boolean result from the function
            
        Raises:
            ScriptException: If the function call fails
        """
        if func_ref not in self.registry:
            raise ScriptException(ExInfo("script command failure")
                .add_info("error", f"Function reference {func_ref} not found"))
        
        try:
            func = self.registry[func_ref]
            result = func(param)
            
            # Check that the result is a boolean
            if not isinstance(result, bool):
                raise ScriptException(ExInfo("script command failure - boolean expected")
                    .add_info("got", type(result).__name__))
            
            return result
        except Exception as e:
            if isinstance(e, ScriptException):
                raise
            raise ScriptException(ExInfo("script command failure")
                .add_info("error", str(e)))
    
    def ref(self, func):
        """
        Store a Lua function in the registry.
        
        Args:
            func: Lua function to store
            
        Returns:
            int: Reference ID for the function
        """
        self.ref_counter += 1
        ref_id = self.ref_counter
        self.registry[ref_id] = func
        return ref_id
    
    def unref(self, func_ref):
        """
        Remove a function from the registry.
        
        Args:
            func_ref (int): Reference to the function
        """
        if func_ref in self.registry:
            del self.registry[func_ref]
    
    def get_global(self, name):
        """
        Get a global variable from the Lua state.
        
        Args:
            name (str): The variable name
            
        Returns:
            The variable value
        """
        return self.state.globals()[name]
        
    def get_registry(self):
        """
        Get the function registry.
        
        Returns:
            dict: The function registry
        """
        return self.registry
