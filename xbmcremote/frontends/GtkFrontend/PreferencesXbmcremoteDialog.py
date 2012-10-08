# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Ben Spiers 
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
This is your preferences dialog.

Define your preferences in
data/glib-2.0/schemas/net.launchpad.xbmcremote.gschema.xml
See http://developer.gnome.org/gio/stable/GSettings.html for more info.
'''

import logging
from socket import gethostbyaddr, herror, gaierror

from gi.repository import Gio, Gtk  # pylint: disable=E0611

from xbmcremote_lib.PreferencesDialog import PreferencesDialog

logger = logging.getLogger('xbmcremote')


class PreferencesXbmcremoteDialog(PreferencesDialog): # pylint: disable=W0232
    '''
    Preferences dialog. Reads and writes preferences to and from GSettings
    '''
    __gtype_name__ = 'PreferencesXbmcremoteDialog'

    def finish_initializing(self, builder):  # pylint: disable=E1002
        '''Set up the preferences dialog'''
        super(PreferencesXbmcremoteDialog, self).finish_initializing(builder)

        # Bind each preference widget to gsettings
        settings = Gio.Settings('net.launchpad.xbmcremote')
        ip_widget = self.builder.get_object('ip_entry')
        port_widget = self.builder.get_object('port_entry')
        version_widget = self.builder.get_object('version_combo')
        mpris_widget = self.builder.get_object('mpris2_check')
        settings.connect('changed', self.on_preferences_changed)
        settings.bind('ip-address', ip_widget,
                      'text', Gio.SettingsBindFlags.DEFAULT)
        settings.bind('port', port_widget,
                      'text', Gio.SettingsBindFlags.DEFAULT)
        settings.bind('version', version_widget,
                      'active', Gio.SettingsBindFlags.DEFAULT)
        settings.bind('mpris2', mpris_widget,
                      'active', Gio.SettingsBindFlags.DEFAULT)

        # Code for other initialization actions should be added here.

    def on_preferences_changed(self, settings, key, data=None):
        '''Validate a change in preferences'''
        if key == 'ip-address':
            # Validate IP address
            try:
                gethostbyaddr(settings.get_string('ip-address'))
            except gaierror:
                logger.debug("Can't resolve host")
                self.ui.invalid_host_label.set_text("Can't resolve host")
                self.ui.invalid_host_label.show()
                self.ui.host_icon.set_from_stock(Gtk.STOCK_NO, 4)
            except herror:
                logger.debug('Invalid host')
                self.ui.invalid_host_label.set_text("Invalid host")
                self.ui.invalid_host_label.show()
                self.ui.host_icon.set_from_stock(Gtk.STOCK_NO, 4)
            else:
                logger.debug('Valid host')
                self.ui.invalid_host_label.hide()
                self.ui.host_icon.set_from_stock(Gtk.STOCK_YES, 4)
        elif key == 'port':
            # Validate port number
            try:
                if 0 < int(settings.get_string('port')) < 65535:
                    logger.debug('Port number in range')
                    self.ui.invalid_port_label.hide()
                    self.ui.port_icon.set_from_stock(Gtk.STOCK_YES, 4)
                else:
                    logger.debug('Port number out of range')
                    self.ui.invalid_port_label.set_text('Port number must be between 1 and 65535')
                    self.ui.invalid_port_label.show()
                    self.ui.port_icon.set_from_stock(Gtk.STOCK_NO, 4)
            except ValueError:
                logger.debug('Port number is not int')
                self.ui.invalid_port_label.set_text('Port number must be an integer')
                self.ui.invalid_port_label.show()
                self.ui.port_icon.set_from_stock(Gtk.STOCK_NO, 4)
