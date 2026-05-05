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
Fish Fillets NG - Python/Pygame version
Main entry point for the game

This is a direct translation of the original C++ main.cpp file.
"""

import sys
import os
import shutil
from game.application import Application
from gengine.log import log_error, log_info
from gengine.ex_info import ExInfo
from gengine.exceptions import HelpException
from gengine.base_exception import BaseException

def main():
    """Main entry point for the game."""
    try:
        app = Application()

        # Use default command line args
        args = sys.argv.copy()
        
        try:
            app.init(args)
            app.run()
        except HelpException as e:
            print(e)
        except BaseException as e:
            log_error(e.info())
            
        app.shutdown()
        return 0
        
    except BaseException as e:
        log_error(e.info())
    except Exception as e:
        log_error(ExInfo("std::exception")
                 .add_info("what", str(e)))
    except:
        log_error(ExInfo("unknown exception"))

    return 1

if __name__ == "__main__":
    sys.exit(main())