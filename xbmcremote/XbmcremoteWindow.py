# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('xbmcremote')

import gtk
import logging
logger = logging.getLogger('xbmcremote')

from xbmcremote_lib import Window
from xbmcremote_lib.Actions import Actions
from xbmcremote_lib.preferences import preferences
from xbmcremote.AboutXbmcremoteDialog import AboutXbmcremoteDialog
from xbmcremote.PreferencesXbmcremoteDialog import PreferencesXbmcremoteDialog

# See xbmcremote_lib.Window.py for more details about how this class works
class XbmcremoteWindow(Window):
    __gtype_name__ = "XbmcremoteWindow"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(XbmcremoteWindow, self).finish_initializing(builder)
        _MYXBMCADDR = preferences.get("ip_entry")
        _MYXBMCPORT = preferences.get("port_entry")
        self.controls = Actions()
        self.AboutDialog = AboutXbmcremoteDialog
        self.PreferencesDialog = PreferencesXbmcremoteDialog
        address_label = self.ui.connected_to
        try:
            self.controls.getSocket(_MYXBMCADDR, int(_MYXBMCPORT))
            address_label.set_label("Connected to: "+_MYXBMCADDR+":"+_MYXBMCPORT)
        except:
            address_label.set_label("Connection Failed!")
        # Code for other initialization actions should be added here.
        self.playerstate = self.controls.sendCustomRequest("AudioPlayer.State", announcement=False)
        
        if self.playerstate.get("paused") == False:
            self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
        else:
            self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)


    def on_playback_play_clicked(self, widget, data=None):
        response = self.controls.PlayPause()
        self.actOnAction(response)

    def on_playback_next_clicked(self, widget, data=None):
        self.controls.PlayNext()

    def on_playback_previous_clicked(self, widget, data=None):
        self.controls.PlayPrevious()

    def on_xbmcremote_window_destroy(self, widget, data=None):
        self.controls.closeSocket()

    def actOnAction(self, action):
        if action == "PlaybackResumed":
            self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
        elif action == "PlaybackPaused":
            self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            