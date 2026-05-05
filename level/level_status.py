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

#\!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Level status module.
"""

import os
from gengine.path import Path

class LevelStatus:
    """
    Level status.
    """
    
    def __init__(self, codename=""):
        """
        Initialize a new level status.
        
        Args:
            codename: The level code name
        """
        self.codename = codename
        self.poster = ""
        self.saved_moves = ""
        self.best_moves = -1
        self.best_author = ""
        self.running = False
        self.complete = False

    def prepare_run(self, codename, poster, best_moves, best_author):
        """Prepare status for a level run."""
        self.complete = False
        self.running = False
        self.codename = codename
        self.poster = poster
        self.best_moves = best_moves
        self.best_author = best_author
    
    def set_current(self, codename):
        """
        Set the current level code name.
        
        Args:
            codename: The level code name
        """
        self.codename = codename
    
    def get_current(self):
        """
        Get the current level code name.
        
        Returns:
            str: The level code name
        """
        return self.codename
    
    def set_running(self, running):
        """
        Set whether the level is running.
        
        Args:
            running: Whether the level is running
        """
        self.running = running
    
    def was_running(self):
        """
        Check if the level was running.
        
        Returns:
            bool: True if the level was running
        """
        return self.running
    
    def set_complete(self):
        """Set the level as complete."""
        self.complete = True
    
    def is_complete(self):
        """
        Check if the level is complete.
        
        Returns:
            bool: True if the level is complete
        """
        return self.complete
    
    @staticmethod
    def get_solution_filename(codename):
        """
        Get the solution filename for a level.
        
        Args:
            codename: The level code name
            
        Returns:
            str: The solution filename
        """
        return os.path.join("solved", f"{codename}.lua")
    
    @staticmethod
    def get_saves_dirname():
        """
        Get the saves directory name.
        
        Returns:
            str: The saves directory name
        """
        return "saves"
    
    @staticmethod
    def save_solution(codename, solution):
        """
        Save a solution for a level.
        
        Args:
            codename: The level code name
            solution: The solution
            
        Returns:
            bool: True if the save was successful
        """
        filename = LevelStatus.get_solution_filename(codename)
        saves_path = Path.data_write_path(filename)
        
        try:
            # Create the directory if it doesnt exist
            dirname = os.path.dirname(saves_path.get_native())
            os.makedirs(dirname, exist_ok=True)
            
            # Write the solution
            with open(saves_path.get_native(), "w") as f:
                f.write(solution)
            
            return True
        except Exception as e:
            from gengine.log import log_warning
            from gengine.ex_info import ExInfo
            log_warning(ExInfo("Failed to save solution")
                       .add_info("filename", filename)
                       .add_info("error", str(e)))
            return False

    def read_moves(self, saved_moves):
        """Store moves read from a solution file."""
        self.saved_moves = saved_moves or ""

    def read_solved_moves(self):
        """Read saved moves for the current level."""
        import re

        self.saved_moves = ""
        solution = Path.data_read_path(self.get_solution_filename(self.codename))
        if solution.exists():
            try:
                with open(solution.get_native(), "r", encoding="utf-8") as f:
                    content = f.read()
                match = re.search(r"saved_moves\s*=\s*(['\"])(.*?)\1", content, re.DOTALL)
                if match:
                    self.saved_moves = match.group(2)
            except OSError:
                self.saved_moves = ""
        return self.saved_moves

    def write_solved_moves(self, moves):
        """Write the best known solution for the current level."""
        previous = self.read_solved_moves()
        if previous and len(previous) <= len(moves):
            return

        file_path = Path.data_write_path(self.get_solution_filename(self.codename))
        dirname = os.path.dirname(file_path.get_native())
        os.makedirs(dirname, exist_ok=True)
        with open(file_path.get_native(), "w", encoding="utf-8") as f:
            f.write(f"\nsaved_moves = '{moves}'\n")

    def compare_to_best(self):
        """
        Compare the player's saved solution to the reference solution.

        Returns:
            int: 1 when the player is better, 0 when equal, -1 when worse.
        """
        moves = len(self.read_solved_moves())
        result = 1
        if self.best_moves > 0:
            if self.best_moves < moves:
                result = -1
            elif self.best_moves == moves:
                result = 0
        return result

    def create_poster(self):
        """Create the optional poster/demo state after finishing a level."""
        if not self.poster:
            return None
        from state.demo_mode import DemoMode
        return DemoMode(Path.data_read_path(self.poster))

    def get_best_moves(self):
        return self.best_moves

    def get_best_author(self):
        return self.best_author
