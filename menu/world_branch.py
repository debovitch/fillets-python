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

import sys
from typing import Optional, Tuple, Dict, List
import re
from gengine.path import Path
from gengine.v2 import V2
from gengine.resource.res_dialog_pack import ResDialogPack
from gengine.log import log_info, log_warning, log_debug
from gengine.ex_info import ExInfo
from gengine.exceptions import LogicException
from menu.level_node import LevelNode
from menu.level_desc import LevelDesc

class WorldBranch:
    """
    Parser for world map files.
    Can read graph of level nodes.
    """
    
    def __init__(self, parent):
        """
        Initialize a new world branch parser.
        
        Args:
            parent: The parent node or None for root
        """
        self.parent = parent
        self.nodes: Dict[str, LevelNode] = {}
        self.root = None
        self.ending = None
        self.out_pack = None
        
        # Register script functions
        self.register_script_functions()
        
    def register_script_functions(self):
        """Register world map script functions."""
        try:
            from gengine.script_agent import ScriptAgent
            from menu.worldmap_script import register_lua_functions
            
            script_agent = ScriptAgent.agent()
            register_lua_functions(script_agent, self)
        except Exception as e:
            sys.exit(f"Failed to register world map script functions: {e}")
    
    def parse_map(self, mapfile: Path, ending_ref, desc_pack: ResDialogPack) -> Optional[LevelNode]:
        """
        Parse a world map file.
        
        Args:
            mapfile: The map file path
            ending_ref: Reference to store the ending node
            desc_pack: Pack to store level descriptions
            
        Returns:
            Optional[LevelNode]: The root node or None on error
        """
        # Store the output parameters
        self.out_pack = desc_pack
        
        # Verify that mapfile is not None or a directory
        if not mapfile or not hasattr(mapfile, 'get_native'):
            log_warning("Invalid map file object")
            self.out_pack = None
            return self._create_demo_map(desc_pack)
            
        import os
        if not os.path.exists(mapfile.get_native()):
            log_warning(f"Map file does not exist: {mapfile.get_native()}")
            self.out_pack = None
            return self._create_demo_map(desc_pack)
            
        if os.path.isdir(mapfile.get_native()):
            log_warning(f"Map file is a directory: {mapfile.get_native()}")
            from gengine.agent.option_agent import OptionAgent
            log_info(f"System dir: {OptionAgent.agent().get_param('systemdir')}")
            log_info(f"User dir: {OptionAgent.agent().get_param('userdir')}")
            self.out_pack = None
            return self._create_demo_map(desc_pack)
        
        # Try to execute the Lua script
        try:
            from gengine.script_agent import ScriptAgent
            ScriptAgent.agent().script_include(mapfile)
            
            # If we have an ending node, store it
            if self.ending and ending_ref is not None:
                ending_ref[0] = self.ending
            
            # Make sure the root node is open if it exists
            if self.root and self.root.get_state() < LevelNode.STATE_OPEN:
                self.root.set_state(LevelNode.STATE_OPEN)
                
            self.out_pack = None
            return self.root
            
        except Exception as e:
            log_warning(ExInfo("Failed to execute Lua script")
                       .add_info("file", mapfile.get_native())
                       .add_info("error", str(e)))
            
            # Fall back to parsing the file manually
            try:
                with open(mapfile.get_native(), 'r') as f:
                    content = f.read()
            except Exception as e:
                log_warning(ExInfo("Cannot read map file")
                           .add_info("file", mapfile.get_native())
                           .add_info("error", str(e)))
                self.out_pack = None
                return self._create_demo_map(desc_pack)
            
            # Parse the map content
            start_node = self._parse_map_content(content, ending_ref, desc_pack)
            
            if not start_node:
                log_warning(ExInfo("Failed to parse map file")
                           .add_info("file", mapfile.get_native()))
                self.out_pack = None
                return self._create_demo_map(desc_pack)
                
            self.out_pack = None
            return start_node
    
    def _parse_map_content(self, content: str, ending_ref, desc_pack: ResDialogPack) -> Optional[LevelNode]:
        """
        Parse the content of a map file.
        
        Args:
            content: The file content
            ending_ref: Reference to store the ending node
            desc_pack: Pack to store level descriptions
            
        Returns:
            Optional[LevelNode]: The root node or None on error
        """
        # This is a simplified parser.
        # In a real implementation, you would parse the file format properly.
        # For now, we just look for specific patterns.
        
        # Find all level definitions
        level_pattern = r'level\s*=\s*\{\s*name\s*=\s*"([^"]+)",\s*file\s*=\s*"([^"]+)",\s*x\s*=\s*(\d+),\s*y\s*=\s*(\d+)'
        
        levels = re.findall(level_pattern, content)
        if not levels:
            return self._create_demo_map(desc_pack)
        
        # Create nodes for all levels
        start_node = None
        for name, file_path, x, y in levels:
            loc = V2(int(x), int(y))
            node = LevelNode(name, Path.data_read_path(file_path), loc)
            
            # Set the first node as the start node
            if not start_node:
                start_node = node
                node.set_state(LevelNode.STATE_OPEN)
            else:
                node.set_state(LevelNode.STATE_FAR)
            
            # Add to the nodes dictionary
            self.nodes[name] = node
            
            # Create a basic description in the description pack
            if hasattr(desc_pack, 'desc'):
                desc_pack.desc.add_desc(name, name, f"Level: {name}")
            elif hasattr(desc_pack, 'add_desc'):
                desc_pack.add_desc(name, name, f"Level: {name}")
        
        # Find all connections
        connection_pattern = r'connection\s*=\s*\{\s*from\s*=\s*"([^"]+)",\s*to\s*=\s*"([^"]+)"'
        
        connections = re.findall(connection_pattern, content)
        for from_name, to_name in connections:
            if from_name in self.nodes and to_name in self.nodes:
                self.nodes[from_name].add_child(self.nodes[to_name])
        
        # Check for ending node
        ending_pattern = r'ending\s*=\s*"([^"]+)"'
        ending_match = re.search(ending_pattern, content)
        if ending_match:
            ending_name = ending_match.group(1)
            if ending_name in self.nodes:
                ending_ref = self.nodes[ending_name]
        
        return start_node
    
    def add_desc(self, codename: str, desc):
        """
        Add a level description.
        
        Args:
            codename: The level code name
            desc: The level description
        
        Raises:
            LogicException: If the out_pack is not set
        """
        if self.out_pack:
            self.out_pack.add_res(codename, desc)
        else:
            raise LogicException(ExInfo("cannot export level description")
                              .add_info("codename", codename))
    
    def add_node(self, parent: str, new_node: LevelNode, hidden: bool):
        """
        Add a new node to the branch.
        
        Args:
            parent: The parent node code name
            new_node: The new node
            hidden: Whether the node is hidden
        """
        self.prepare_node(new_node, hidden)
        self.insert_node(parent, new_node)
    
    def set_ending(self, new_node: LevelNode):
        """
        Set the ending node.
        
        Args:
            new_node: The ending node
        """
        if self.ending:
            # In Python we don't need to delete the old node explicitly
            pass
            
        self.ending = new_node
        
        if self.was_solved(new_node.get_codename()):
            new_node.set_state(LevelNode.STATE_SOLVED)
        else:
            new_node.set_state(LevelNode.STATE_OPEN)
            
        new_node.set_depth(-1)
    
    def best_solution(self, codename: str, moves: int, author: str):
        """
        Store the best solution.
        
        Args:
            codename: The level code name
            moves: The number of moves
            author: The solution author
        """
        if self.root:
            node = self.root.find_named(codename)
            if node:
                node.best_solution(moves, author)
            else:
                log_warning(ExInfo("there is no such node")
                           .add_info("codename", codename)
                           .add_info("moves", moves)
                           .add_info("author", author))
    
    def was_solved(self, codename: str) -> bool:
        """
        Check if a level was solved.
        
        Args:
            codename: The level code name
            
        Returns:
            bool: True if the level was solved
        """
        # In the original this references LevelStatus::getSolutionFilename
        # We'll use a simple check for now
        from level.level_status import LevelStatus
        if hasattr(LevelStatus, 'get_solution_filename'):
            filename = LevelStatus.get_solution_filename(codename)
            solved = Path.data_read_path(filename)
            return Path.check_exists(solved)
        return False
    
    def prepare_node(self, node: LevelNode, hidden: bool):
        """
        Set the node state.
        
        Args:
            node: The node
            hidden: Whether the node is hidden
        """
        if self.was_solved(node.get_codename()):
            node.set_state(LevelNode.STATE_SOLVED)
        elif hidden:
            node.set_state(LevelNode.STATE_HIDDEN)
        else:
            node.set_state(LevelNode.STATE_FAR)
    
    def insert_node(self, parent: str, new_node: LevelNode):
        """
        Insert a node as a parent's child.
        
        Args:
            parent: The parent node code name
            new_node: The new node
            
        Raises:
            LogicException: If there is an error inserting the node
        """
        try:
            if parent == "" and self.root:
                raise LogicException(ExInfo("there is a one root node already")
                                  .add_info("root", self.root.get_codename())
                                  .add_info("new_node", new_node.get_codename()))
            
            if self.root:
                parent_node = self.root.find_named(parent)
                if parent_node:
                    parent_node.add_child(new_node)
                else:
                    raise LogicException(ExInfo("there is no such parent node")
                                      .add_info("parent", parent)
                                      .add_info("new_node", new_node.get_codename()))
            else:
                if parent != "":
                    log_warning(ExInfo("root node should have empty parent")
                               .add_info("parent", parent)
                               .add_info("new_node", new_node.get_codename()))
                self.root = new_node
        except Exception as e:
            # In Python we don't need to delete the node explicitly
            raise e
    
    def _create_demo_map(self, desc_pack: ResDialogPack) -> LevelNode:
        """
        Create a simple demo map.
        
        Args:
            desc_pack: Pack to store level descriptions
            
        Returns:
            LevelNode: The root node
        """
        # Create a simple demo map structure with two levels
        root = LevelNode("demo1", Path.data_read_path("levels/demo1.lua"), V2(300, 300))
        root.set_state(LevelNode.STATE_OPEN)
        
        level2 = LevelNode("demo2", Path.data_read_path("levels/demo2.lua"), V2(500, 300))
        level2.set_state(LevelNode.STATE_FAR)
        
        # Connect levels
        root.add_child(level2)
        
        # Set as the root node
        self.root = root
        
        # Add demo level descriptions
        if hasattr(desc_pack, 'desc'):
            desc_pack.desc.add_desc("demo1", "Demo Level 1", "This is the first demo level")
            desc_pack.desc.add_desc("demo2", "Demo Level 2", "This is the second demo level")
        elif hasattr(desc_pack, 'add_desc'):
            desc_pack.add_desc("demo1", "Demo Level 1", "This is the first demo level")
            desc_pack.add_desc("demo2", "Demo Level 2", "This is the second demo level")
        
        return root
