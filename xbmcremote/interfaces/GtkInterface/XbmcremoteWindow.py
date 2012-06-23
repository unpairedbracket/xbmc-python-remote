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

import gettext
from gettext import gettext as _
gettext.textdomain('xbmcremote')

from gi.repository import Gtk
import logging
logger = logging.getLogger('xbmcremote')

from xbmcremote_lib import Window
from AboutXbmcremoteDialog import AboutXbmcremoteDialog
from PreferencesXbmcremoteDialog import PreferencesXbmcremoteDialog
from ErrorDialog import ErrorDialog

# See xbmcremote_lib.Window.py for more details about how this class works
class XbmcremoteWindow(Window):
    __gtype_name__ = 'XbmcremoteWindow'
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        '''Set up the main window'''
        super(XbmcremoteWindow, self).finish_initializing(builder)
        self.gui = True
        self.AboutDialog = AboutXbmcremoteDialog
        self.PreferencesDialog = PreferencesXbmcremoteDialog
        self.ErrorDialog = ErrorDialog
        # Code for other initialization actions should be added here.
        self.artistid = self.albumid = self.songid = -1
        
    def set_interface(self, interface):
        self.interface = interface
        self.controller = interface.controller
    
    def join_args(self, *args):
        strs = map(str, args)
        string = ' '.join(strs)
        return string

    def newArtist(self, widget, data=None):
        if data != []:
            self.artistid = data[0]['artistid']
            self.albumid = -1
#            self.controller.GetAlbums(self.artistid)
            self.interface.emit("xbmc_get", "albums", self.join_args(self.artistid))
#            self.controller.GetSongs(self.artistid, self.albumid)
            self.interface.emit("xbmc_get", "songs", self.join_args(self.artistid, self.albumid))

    def newAlbum(self, widget, data=None):
        if data != []:
            self.albumid = data[0]['albumid']
#            self.controller.GetSongs(self.artistid, self.albumid)
            self.interface.emit("xbmc_get", "songs", self.join_args(self.artistid, self.albumid))

    def newSong(self, widget, data=None):
        if data != []:
            self.songid = data[0]['songid']

    def on_playback_play_clicked(self, widget, data=None):
        if self.controller.playing:
            self.interface.emit("xbmc_control", "play", None)
        else:
            self.interface.emit("xbmc_control", "start", None)

    def on_playback_next_clicked(self, widget, data=None):
        self.interface.emit("xbmc_control", "next", None)

    def on_playback_previous_clicked(self, widget, data=None):
        self.interface.emit("xbmc_control", "prev", None)

    def on_refresh_clicked(self, widget, data=None):
        self.interface.refresh(True)

    def on_xbmcremote_window_destroy(self, widget, data=None):
        self.controller.kill()
        Gtk.main_quit()
