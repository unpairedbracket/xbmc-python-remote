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
This is the main window of the GTK frontend. It should only be
instantiated used through the GtkFrontend, not on its own.
'''
# pylint: disable=W0201,C0103,W0232
import gettext
_ = gettext.gettext
gettext.textdomain('xbmcremote')

import logging
logger = logging.getLogger('xbmcremote')

from gi.repository import Gtk

from xbmcremote_lib import Window
from AboutXbmcremoteDialog import AboutXbmcremoteDialog
from PreferencesXbmcremoteDialog import PreferencesXbmcremoteDialog
from ErrorDialog import ErrorDialog


class XbmcremoteWindow(Window):

    '''
    See xbmcremote_lib.Window.py for more details about how this class works
    '''

    __gtype_name__ = 'XbmcremoteWindow'

    def finish_initializing(self, builder):  # pylint: disable=E1002
        '''Set up the main window'''
        super(XbmcremoteWindow, self).finish_initializing(builder)
        self.AboutDialog = AboutXbmcremoteDialog
        self.PreferencesDialog = PreferencesXbmcremoteDialog
        self.ErrorDialog = ErrorDialog
        # Code for other initialization actions should be added here.
        self.info = {'artistid': -1, 'albumid': -1, 'songid': -1}
        self.application = None
        self.frontend = None

    def set_frontend(self, frontend):
        '''
        Set the owning instance of GtkFrontend.

        Can't do this in a constructor because multiple inheritance
        gets really messy when classes have their own __new__ defined
        '''

        self.frontend = frontend
        self.application = frontend.application

    def new_artist(self, widget, data=None):
        '''Send the appropriate signals when a new artist is selected'''
        if data != []:
            self.info['artistid'] = data[0]['artistid']
            self.info['albumid'] = -1

            params = {'artistid': self.info['artistid']}
            self.frontend.emit("xbmc_control", "albums", params)

            params = {'artistid': self.info['artistid'],
                      'albumid': self.info['albumid']}
            self.frontend.emit("xbmc_control", "songs", params)

    def new_album(self, widget, data=None):
        '''Send the appropriate signals when a new album is selected'''
        if data != []:
            self.info['albumid'] = data[0]['albumid']
            params = {'artistid': self.info['artistid'],
                      'albumid': self.info['albumid']}
            self.frontend.emit("xbmc_control", "songs", params)

    def new_song(self, widget, data=None):
        '''Send the appropriate signals when a new song is selected'''
        if data != []:
            self.info['songid'] = data[0]['songid']

    def on_playback_play_clicked(self, widget, data=None):
        '''Signal handler for the play button'''
        if self.frontend.state['playing']:
            self.frontend.emit("xbmc_control", "play", None)
        else:
            self.frontend.emit("xbmc_control", "start", None)

    def on_playback_next_clicked(self, widget, data=None):
        '''Signal handler for the skip next button'''
        self.frontend.emit("xbmc_control", "next", None)

    def on_playback_previous_clicked(self, widget, data=None):
        '''Signal handler for the skip back button'''
        self.frontend.emit("xbmc_control", "prev", None)

    def on_refresh_clicked(self, widget, data=None):
        '''Signal handler for the refresh button'''
        self.frontend.emit('xbmc_reconnect')

    def on_play_now_clicked(self, widget, data=None):
        if self.info['songid'] != -1:
            params = {'songid': self.info['songid']}
            self.frontend.emit('xbmc_control', 'play_now', params)

    def on_play_next_activate(self, widget, data=None):
        if self.info['songid'] != -1:
            params = {'songid': self.info['songid']}
            self.frontend.emit('xbmc_control', 'play_next', params)

    def on_play_last_activate(self, widget, data=None):
        if self.info['songid'] != -1:
            params = {'songid': self.info['songid']}
            self.frontend.emit('xbmc_control', 'play_last', params)

    def on_xbmcremote_window_destroy(self, widget, data=None):
        '''Signal handler for destruction of the window'''
        self.frontend.emit('xbmc_kill')
        Gtk.main_quit()
