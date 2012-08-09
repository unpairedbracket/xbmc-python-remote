# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Ben Spiers
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from gi.repository import GObject

class Signals(GObject.GObject):
    __gsignals__ = {
            "xbmc_init": (GObject.SIGNAL_RUN_FIRST, None, ()),
            "xbmc_send": (GObject.SIGNAL_RUN_FIRST, None, (str, float)),
            "xbmc_new_playing": (GObject.SIGNAL_RUN_FIRST, None, (str, str, str)),
            "xbmc_error": (GObject.SIGNAL_RUN_FIRST, None, (str, int, str)),
            "xbmc_received": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
            "xbmc_get": (GObject.SIGNAL_RUN_FIRST, None, (str, str,)),
            "xbmc_control": (GObject.SIGNAL_RUN_FIRST, None, (str, str,)),
            "xbmc_connected": (GObject.SIGNAL_RUN_FIRST, None, ())
        }
