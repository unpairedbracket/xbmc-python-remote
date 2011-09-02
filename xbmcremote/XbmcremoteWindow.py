# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('xbmcremote')

import gtk
import gobject
import logging
logger = logging.getLogger('xbmcremote')

from quickly.widgets.dictionary_grid import DictionaryGrid
from quickly.widgets.grid_column import IntegerColumn

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
        _MYXBMCADDR = preferences["ip_entry"]
        _MYXBMCPORT = preferences["port_entry"]
        self.controls = Actions()
        self.AboutDialog = AboutXbmcremoteDialog
        self.PreferencesDialog = PreferencesXbmcremoteDialog
        address_label = self.ui.connected_to
        try:
            self.controls.getSocket(_MYXBMCADDR, int(_MYXBMCPORT))
            address_label.set_label("Connected to: "+_MYXBMCADDR+":"+_MYXBMCPORT)
            self.connected = True
        except:
            address_label.set_label("Connection Failed!")
            self.connected = False
        # Code for other initialization actions should be added here.
        self.updatePlaying()
        gobject.timeout_add(1000, self.updatePlaying)
        self.artistid = self.albumid = self.songid = -1
        self.updateLibrary()
        
    def updateLibrary(self):
        self.getArtists()
        self.getAlbums()
        self.getSongs()
    
    def updatePlaying(self):
        try:
            self.playerstate = self.controls.sendCustomRequest("AudioPlayer.State", announcement=False)   
            if self.playerstate["paused"] == False:
                self.playing = True
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
            elif self.playerstate["paused"] == True:
                self.playing = True
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            else:
                self.playing = False
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            return True
        finally:
            return True
    
    def getArtists(self):
        artistlist = self.ui.artist_list
        artists = self.controls.GetArtists()['artists']
        
        artist_grid = DictionaryGrid(artists, keys=['label'])
        artist_grid.columns['label'].set_title("Artist")
        artist_grid.connect("selection_changed", self.newArtist)
        artist_grid.show()
        
        artistlist.add(artist_grid)
    
    def getAlbums(self):
        albumlist = self.ui.album_list
        
        for c in albumlist.get_children():
            albumlist.remove(c)
        
        albums = self.controls.GetAlbums(self.artistid)['albums']
        
        album_grid = DictionaryGrid(albums, keys=['label'])
        album_grid.columns['label'].set_title("Album")
        album_grid.connect("selection_changed", self.newAlbum)
        album_grid.show()
        
        albumlist.add(album_grid)
    
    def getSongs(self):
        songlist = self.ui.song_list
        
        for c in songlist.get_children():
            songlist.remove(c)

        songs = self.controls.GetSongs(self.artistid, self.albumid)['songs']
        
        song_grid = DictionaryGrid(songs, keys=['label'])
        song_grid.columns['label'].set_title("Title")
        song_grid.connect("selection_changed", self.newSong)
        song_grid.show()
        
        songlist.add(song_grid)
    
    def newArtist(self, widget, data=None):
        self.artistid = data[0]['artistid']
        self.albumid = -1
        self.getAlbums()
        self.getSongs()

    def newAlbum(self, widget, data=None):
        self.albumid = data[0]['albumid']
        self.getSongs()

    def newSong(self, widget, data=None):
        self.songid = data[0]['songid']

    def on_playback_play_clicked(self, widget, data=None):
        if not self.playing:
            response = self.controls.StartPlaying()
        else:
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
            
            