# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Ben Spiers # This program is free software: you can redistribute it and/or modify it 
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

# This is your preferences dialog.
#
# Define your preferences in
# data/glib-2.0/schemas/net.launchpad.xbmcremote.gschema.xml
# See http://developer.gnome.org/gio/stable/GSettings.html for more info.

from gi.repository import Gio # pylint: disable=E0611

import gettext
from gettext import gettext as _
gettext.textdomain('xbmcremote')

import logging
logger = logging.getLogger('xbmcremote')

from xbmcremote_lib.PreferencesDialog import PreferencesDialog

class PreferencesXbmcremoteDialog(PreferencesDialog):
    __gtype_name__ = 'PreferencesXbmcremoteDialog'

    def finish_initializing(self, builder): # pylint: disable=E1002
        '''Set up the preferences dialog'''
        super(PreferencesXbmcremoteDialog, self).finish_initializing(builder)

        # Bind each preference widget to gsettings
        settings = Gio.Settings('net.launchpad.xbmcremote')
        ip_widget = self.builder.get_object('ip_entry')
        port_widget = self.builder.get_object('port_entry')
        version_widget = self.builder.get_object('version_combo')
        mpris_widget = self.builder.get_object('mpris2_check')
        settings.bind('ip-address', ip_widget, 'text', Gio.SettingsBindFlags.DEFAULT)
        settings.bind('port', port_widget, 'text', Gio.SettingsBindFlags.DEFAULT)
        settings.bind('version', version_widget, 'active', Gio.SettingsBindFlags.DEFAULT)
        settings.bind('mpris2', mpris_widget, 'active', Gio.SettingsBindFlags.DEFAULT)

        # Code for other initialization actions should be added here.
