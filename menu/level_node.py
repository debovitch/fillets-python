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

from typing import List, Optional
import pygame
from gengine.v2 import V2
from gengine.path import Path
from gengine.no_copy import NoCopy
from level.level import Level

class LevelNode(NoCopy):
    """
    Node on the world map representing a level.
    """
    
    # State constants
    STATE_HIDDEN = 0
    STATE_FAR = 1
    STATE_OPEN = 2
    STATE_SOLVED = 3
    
    # Display constants
    DOT_RADIUS = 13
    
    def __init__(self, codename: str, datafile: Path, loc: V2, poster: str = ""):
        """
        Initialize a level node.
        
        Args:
            codename: The code name of the level
            datafile: The path to the level data file
            loc: The location on the map
            poster: The poster image file (optional)
        """
        self.codename = codename
        self.poster = poster
        self.datafile = datafile
        self.loc = loc
        self.state = LevelNode.STATE_FAR
        self.depth = 1
        self.children: List[LevelNode] = []
        self.best_moves = -1
        self.best_author = ""
    
    def set_state(self, state: int) -> None:
        """
        Set the state of this node.
        
        Args:
            state: The new state
        """
        if state == LevelNode.STATE_SOLVED:
            for child in self.children:
                if child.get_state() < LevelNode.STATE_OPEN:
                    child.set_state(LevelNode.STATE_OPEN)

        self.state = state
    
    def get_state(self) -> int:
        """
        Get the state of this node.
        
        Returns:
            int: The state
        """
        return self.state
    
    def set_depth(self, depth: int) -> None:
        """
        Set the depth of this node.
        
        Args:
            depth: The new depth
        """
        self.depth = depth
    
    def get_depth(self) -> int:
        """
        Get the depth of this node.
        
        Returns:
            int: The depth
        """
        return self.depth
    
    def best_solution(self, moves: int, author: str) -> None:
        """
        Set the best solution for this level.
        
        Args:
            moves: The number of moves
            author: The author of the solution
        """
        self.best_moves = moves
        self.best_author = author
    
    def get_best_moves(self) -> int:
        """
        Get the best number of moves.
        
        Returns:
            int: The best number of moves
        """
        return self.best_moves
    
    def get_best_author(self) -> str:
        """
        Get the best solution author.
        
        Returns:
            str: The best solution author
        """
        return self.best_author
    
    def get_codename(self) -> str:
        """
        Get the code name of this level.
        
        Returns:
            str: The code name
        """
        return self.codename
    
    def get_loc(self) -> V2:
        """
        Get the location of this node.
        
        Returns:
            V2: The location
        """
        return self.loc
    
    def get_poster(self) -> str:
        """
        Get the poster image file.
        
        Returns:
            str: The poster image file
        """
        return self.poster
    
    def create_level(self) -> Level:
        """
        Create a level from this node.
        
        Returns:
            Level: The created level
        """
        return Level(self.codename, self.datafile, self.depth)
    
    def add_child(self, new_node: 'LevelNode') -> None:
        """
        Add a child node to this node.
        
        Args:
            new_node: The child node to add
        """
        self.children.append(new_node)
        new_node.set_depth(self.depth + 1)
        if self.state == LevelNode.STATE_SOLVED and new_node.get_state() < LevelNode.STATE_OPEN:
            new_node.set_state(LevelNode.STATE_OPEN)
    
    def is_under(self, cursor: V2) -> bool:
        """
        Check if a cursor is over this node.
        
        Args:
            cursor: The cursor position
            
        Returns:
            bool: True if the cursor is over this node
        """
        diff = self.loc.minus(cursor)
        distance = diff.get_x() ** 2 + diff.get_y() ** 2
        return distance < (LevelNode.DOT_RADIUS ** 2)
    
    def find_selected(self, cursor: V2) -> Optional['LevelNode']:
        """
        Find a selected node under the cursor.
        
        Args:
            cursor: The cursor position
            
        Returns:
            Optional[LevelNode]: The selected node or None
        """
        if self.state >= LevelNode.STATE_OPEN:
            if self.is_under(cursor):
                return self

            for child in self.children:
                selected = child.find_selected(cursor)
                if selected:
                    return selected
        
        return None
    
    def find_open_nodes(self) -> List['LevelNode']:
        """
        Find all open nodes.
        
        Returns:
            List[LevelNode]: List of open nodes
        """
        result = []
        if self.state >= LevelNode.STATE_OPEN:
            if self.state == LevelNode.STATE_OPEN:
                result.append(self)

            for child in self.children:
                result.extend(child.find_open_nodes())
        
        return result
    
    def find_next_open(self, current: Optional['LevelNode']) -> Optional['LevelNode']:
        """
        Find the next open node after the current one.
        
        Args:
            current: The current node
            
        Returns:
            Optional[LevelNode]: The next open node or None
        """
        open_nodes = self.find_open_nodes()
        if not open_nodes:
            return None
        
        if not current:
            return open_nodes[0]
        
        # Find current in the list and return the next one
        for i, node in enumerate(open_nodes):
            if node == current:
                if i + 1 < len(open_nodes):
                    return open_nodes[i + 1]
                else:
                    return open_nodes[0]
        
        return open_nodes[0]
    
    def find_named(self, codename: str) -> Optional['LevelNode']:
        """
        Find a node by its code name.
        
        Args:
            codename: The code name to find
            
        Returns:
            Optional[LevelNode]: The found node or None
        """
        if self.codename == codename:
            return self
        
        for child in self.children:
            found = child.find_named(codename)
            if found:
                return found
        
        return None
    
    def are_all_solved(self) -> bool:
        """
        Check if all nodes are solved.
        
        Returns:
            bool: True if all nodes are solved
        """
        if self.state != LevelNode.STATE_SOLVED:
            return False
        
        for child in self.children:
            if not child.are_all_solved():
                return False
        
        return True
    
    def is_leaf(self) -> bool:
        """
        Check if this node is a leaf node.
        
        Returns:
            bool: True if this node is a leaf
        """
        return not self.children
    
    def draw_path(self, drawer) -> None:
        """
        Draw the path from this node to its children.
        
        Args:
            drawer: The node drawer
        """
        if self.state > LevelNode.STATE_HIDDEN:
            for child in self.children:
                if child.get_state() > LevelNode.STATE_HIDDEN:
                    drawer.draw_edge(self, child)
                    child.draw_path(drawer)
            drawer.draw_node(self)
