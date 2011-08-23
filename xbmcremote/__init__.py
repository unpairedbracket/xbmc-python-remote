# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('xbmcremote')

import gtk

from xbmcremote import XbmcremoteWindow, xbmc

from xbmcremote_lib import set_up_logging, preferences, get_version

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs xbmcremote_lib also)"))
    parser.add_option(
        "-t", "--no_gui", action="store_false", dest="gui",
        help=_("Run in terminal."))
    parser.add_option(
        "-g", "--gui", action="store_true", dest="gui",
        help=_("Run with gui. This is the default option"))
    parser.set_defaults(gui=True)
    (options, args) = parser.parse_args()

    set_up_logging(options)
    return options

def main():
    'constructor for your class instances'
    options = parse_options()
    # preferences
    # set some values for our first session
    # TODO: replace defaults with your own values
    default_preferences = {
    'ip_entry': '192.168.0.1',
    'port_entry': '9090',
    }
    preferences.update(default_preferences)
    # user's stored preferences are used for 2nd and subsequent sessions
    preferences.db_connect()
    preferences.load()
    if options.gui:
        # Run the application.
        window = XbmcremoteWindow.XbmcremoteWindow()
        window.show()
        gtk.main()
    else:
        xbmc.main()

    preferences.save()
