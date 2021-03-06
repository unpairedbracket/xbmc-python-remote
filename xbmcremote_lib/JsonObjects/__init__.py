# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Ben Spiers 
# 
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

'''
Imports the appropriate version of the JSON API. Dharma isn't really
supported any more, it probably doesn't even work.
'''

from gi.repository import Gio

settings = Gio.Settings("net.launchpad.xbmcremote")

if settings.get_int('version') == 0:
    from EdenJsonObjects import JsonRpc
elif settings.get_int('version') == 1:
    from FrodoJsonObjects import JsonRpc

xbmc_json = JsonRpc()
