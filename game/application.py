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
Main application class for Fish Fillets NG.
"""

import pygame
import sys
from gengine.no_copy import NoCopy
from gengine.agent.base_listener import BaseListener
from gengine.name import Name
from gengine.agent.agent_pack import AgentPack
from gengine.log import log_debug, log_warning, log_error, Log
from gengine.random import Random
from gengine.script_agent import ScriptAgent
from gengine.agent.option_agent import OptionAgent
from gengine.agent.video_agent import VideoAgent
from gengine.agent.input_agent import InputAgent
from gengine.agent.timer_agent import TimerAgent
from gengine.agent.messager_agent import MessagerAgent
from gengine.path import Path
from gengine.message.simple_msg import SimpleMsg
from gengine.message.string_msg import StringMsg
from gengine.ex_info import ExInfo
from gengine.exceptions import ResourceException
from plan.subtitle_agent import SubTitleAgent
from game.game_agent import GameAgent

class Application(NoCopy, BaseListener):
    """
    Main application class.
    Initializes and manages all game components.
    """
    
    def __init__(self):
        """Initialize the application."""
        NoCopy.__init__(self)
        self.quit = False
        Random.init()
        
        # Initialize pygame
        pygame.init()
        
        # Initialize agent pack
        self.agents = AgentPack()
        
        # Add agents in the same order as the C++ version
        self.agents.add_agent(ScriptAgent())
        self.agents.add_agent(OptionAgent())
        self.agents.add_agent(VideoAgent())
        self.agents.add_agent(InputAgent())
        self.agents.add_agent(SubTitleAgent())
        self.agents.add_agent(GameAgent())
        self.agents.add_agent(TimerAgent())
    
    def get_name(self):
        """
        Get the application name.
        
        Returns:
            str: The application name
        """
        return Name.APP_NAME
    
    def init(self, args=None):
        """
        Initialize the application.
        
        Args:
            args: Command line arguments (optional)
        """
        MessagerAgent.agent().add_listener(self)
        self.agents.init(Name.VIDEO_NAME)
        self.prepare_log_level()
        self.prepare_options(args)
        self.customize_game()
        
        self.agents.init(Name.TIMER_NAME)
        self.add_sound_agent()
        
        self.agents.init()
        GameAgent.get_instance().manager.handle_next_state()
    
    def run(self):
        """Run the main application loop."""
        while not self.quit:
            self.agents.update()
    
    def shutdown(self):
        """Shutdown the application."""
        self.agents.shutdown()
        pygame.quit()
    
    def prepare_log_level(self):
        """Set log level according to options."""
        options = OptionAgent.agent()
        event = StringMsg(self, "param_changed", "loglevel")
        options.add_watcher("loglevel", event)
        options.set_default("loglevel", Log.get_log_level())
    
    def prepare_options(self, args=None):
        """
        Prepare options for the application.
        
        Args:
            args: Command line arguments (optional)
        """
        import os
        options = OptionAgent.agent()
        
        # Define all options with their types and descriptions
        options.add_param("loglevel", "number", "Debug with loglevel 7 (default=6)")
        options.add_param("systemdir", "path", "Path to game data")
        options.add_param("userdir", "path", "Path to game data")
        options.add_param("lang", "string", "2-letter code (e.g., en, cs, fr, de)")
        options.add_param("speech", "string", "Lang for speech")
        options.add_param("subtitles", "boolean", "Enable subtitles")
        options.add_param("fullscreen", "boolean", "Turn fullscreen on/off")
        options.add_param("show_steps", "boolean", "Show a step counter in levels")
        options.add_param("sound", "boolean", "Turn sound on/off")
        options.add_param("volume_sound", "number", "Sound volume in percentage")
        options.add_param("volume_music", "number", "Music volume in percentage")
        options.add_param("worldmap", "string", "Path to the worldmap file")
        options.add_param("cache_images", "boolean", "Cache images (default=true)")
        options.add_param("sound_frequency", "number", "Sound sample rate (default=44100)")
        options.add_param("strict_rules", "boolean", "Disallow pushing of partially supported objects (default=true)")
        options.add_param("replay_level", "string", "Replay the solution for the given level codename")

        options.set_default("show_steps", "1")
        
        # Parse command line options
        if args:
            options.parse_cmd_opt(args)
            
        # Set default directories if not provided
        if not options.get_param("systemdir"):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(base_dir, "data")
            options.set_param("systemdir", data_dir)
            from gengine.log import log_info
            log_info(f"Using default system dir: {data_dir}")
            
        if not options.get_param("userdir"):
            # Use the user_data directory in the project
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            user_dir = os.path.join(base_dir, "user_data")
            os.makedirs(user_dir, exist_ok=True)
            options.set_param("userdir", user_dir)
            from gengine.log import log_info
            log_info(f"Using default user dir: {user_dir}")
    
    def customize_game(self):
        """
        Run the initialization script.
        
        Raises:
            ResourceException: When data files are not available
        """
        import os
        initfile = Path.data_read_path("script/init.lua")
        
        if Path.check_exists(initfile):
            ScriptAgent.agent().script_include(initfile)
        else:
            options = OptionAgent.agent()
            # Try direct access
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            direct_path = os.path.join(base_dir, "data", "script", "init.lua")
            
            if os.path.exists(direct_path):
                ScriptAgent.agent().script_include(Path(direct_path))
            else:
                raise ResourceException(ExInfo("init file not found")
                    .add_info("path", initfile.get_native())
                    .add_info("systemdir", options.get_param("systemdir"))
                    .add_info("userdir", options.get_param("userdir"))
                    .add_info("hint", "try command line option \"systemdir=path/to/data\""))
    
    def add_sound_agent(self):
        """
        Choose appropriate sound agent based on the 'sound' config option.
        """
        from gengine.agent.dummy_sound_agent import DummySoundAgent
        from gengine.agent.pygame_sound_agent import PygameSoundAgent
        
        options = OptionAgent.agent()
        
        if options.get_as_bool("sound", True):
            sound_agent = PygameSoundAgent()
            try:
                sound_agent.init()
            except Exception as e:
                log_warning(f"Failed to initialize sound: {e}")
                sound_agent = DummySoundAgent()
        else:
            sound_agent = DummySoundAgent()
        
        self.agents.add_agent(sound_agent)
    
    def receive_simple(self, msg):
        """
        Handle simple messages.
        
        Args:
            msg (SimpleMsg): The message to handle
        """
        if msg.equals_name("quit"):
            self.quit = True
        
        elif msg.equals_name("inc_loglevel"):
            level = Log.get_log_level() + 1
            if level <= Log.LEVEL_DEBUG:
                OptionAgent.agent().set_param("loglevel", level)
        
        elif msg.equals_name("dec_loglevel"):
            level = Log.get_log_level() - 1
            if level >= Log.LEVEL_ERROR:
                OptionAgent.agent().set_param("loglevel", level)
        
        elif msg.equals_name("flush_stdout"):
            sys.stdout.flush()
        
        else:
            log_warning(ExInfo("unknown msg").add_info("msg", msg.to_string()))
    
    def receive_string(self, msg):
        """
        Handle string messages.
        
        Args:
            msg (StringMsg): The message to handle
        """
        if msg.equals_name("param_changed"):
            param = msg.get_value()
            if param == "loglevel":
                Log.set_log_level(OptionAgent.agent().get_as_int("loglevel"))
        else:
            log_warning(ExInfo("unknown msg").add_info("msg", msg.to_string()))
