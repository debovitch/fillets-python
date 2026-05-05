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

from gengine.agent.sound_agent import SoundAgent

class DummySoundAgent(SoundAgent):
    """
    Dummy sound agent that doesn't play any sounds.
    Used when the sound system cannot be initialized.
    """
    
    def __init__(self):
        """
        Initialize the dummy sound agent.
        """
        super().__init__()
    
    def set_sound_volume(self, volume):
        """
        Set the sound effects volume (does nothing).
        
        Args:
            volume (int): Volume level (0-100)
        """
        pass
    
    def set_music_volume(self, volume):
        """
        Set the music volume (does nothing).
        
        Args:
            volume (int): Volume level (0-100)
        """
        pass
    
    def play_sound(self, sound, volume, loops=0):
        """
        Play a sound effect (does nothing).
        
        Args:
            sound: The sound to play
            volume (int): Volume level for this sound (0-100)
            loops (int): Number of times to repeat the sound
        
        Returns:
            int: Always returns -1 (no channel)
        """
        return -1
    
    def play_music(self, file_path, finished_msg=None):
        """
        Play music from a file (does nothing).
        
        Args:
            file_path: Path to the music file
            finished_msg: Message to send when music finishes playing
        """
        # Just discard the message
        if finished_msg:
            del finished_msg
    
    def stop_music(self):
        """
        Stop currently playing music (does nothing).
        """
        pass