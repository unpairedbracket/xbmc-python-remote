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
xbmcremote package: contains most of the important parts of the program.
See also: xbmcremote_lib
'''

import optparse

import locale
locale.textdomain('xbmcremote')

from Application import Application
from xbmcremote_lib import set_up_logging, get_version
from dbus.mainloop.glib import DBusGMainLoop

def parse_options():
    '''Support for command line options'''
    parser = optparse.OptionParser(version='%%prog %s' % get_version())
    parser.add_option(
        '-v', '--verbose', action='count', dest='verbose',
        help=('Show debug messages (-vv debugs xbmcremote_lib also)'))
    parser.add_option(
        '-t', '--no_gui', action='store_false', dest='gui',
        help=('Run in terminal.'))
    parser.add_option(
        '-g', '--gui', action='store_true', dest='gui',
        help=('Run with gui. This is the default option'))
    parser.set_defaults(gui=True)
    options = parser.parse_args()

    set_up_logging(options[0])
    return options[0]

def main():
    '''Turn on the DBus Mainloop and start the program'''
    #turn on the dbus mainloop
    DBusGMainLoop(set_as_default=True)

    #constructor for your class instances
    options = parse_options()

    app = Application(options.gui)
    app.start_app()
