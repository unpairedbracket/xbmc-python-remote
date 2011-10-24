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

from threading import Thread

# See xbmcremote_lib.Window.py for more details about how this class works
class XbmcremoteWindow(Window):
    __gtype_name__ = 'XbmcremoteWindow'

    def finish_initializing(self, builder): # pylint: disable=E1002
        '''Set up the main window'''
        super(XbmcremoteWindow, self).finish_initializing(builder)
        _MYXBMCADDR = preferences['ip_entry']
        _MYXBMCPORT = preferences['port_entry']
        self.controls = Actions()
        self.AboutDialog = AboutXbmcremoteDialog
        self.PreferencesDialog = PreferencesXbmcremoteDialog
        address_label = self.ui.connected_to
        try:
            self.controls.getSocket(_MYXBMCADDR, int(_MYXBMCPORT))
            address_label.set_label('Connected to: '+_MYXBMCADDR+':'+_MYXBMCPORT)
            self.connected = True
        except:
            address_label.set_label('Connection Failed!')
            self.connected = False
        # Code for other initialization actions should be added here.
        gobject.threads_init()
        self.artistid = self.albumid = self.songid = -1
        if self.connected:
            Thread(target=self.updateLibrary).start()
        self.playing = False
        self.updatePlaying()
        gobject.timeout_add(1000, self.updatePlaying)
        
    def updateLibrary(self):
        self.getArtists()
        self.getAlbums()
        self.getSongs()
    
    def updatePlaying(self):
        try:
            self.playerstate = self.controls.sendCustomRequest('AudioPlayer.State', announcement=False)
            if self.playerstate['type'] != 'response':
                pass
            elif self.playerstate['data']['paused'] == False:
                self.playing = True
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
            elif self.playerstate['data']['paused'] == True:
                self.playing = True
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            else:
                self.playing = False
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            return True
        finally:
            return True
    
    def getArtists(self):
        artistview = self.ui.artist_list
        
        while True:
            artistlist = self.controls.GetArtists()
            if artistlist['type'] == 'response':
                break
        artists = artistlist['data']['artists']
        
        artist_grid = DictionaryGrid(artists, keys=['label'])
        artist_grid.columns['label'].set_title('Artist')
        artist_grid.connect('selection_changed', self.newArtist)
        artist_grid.show()
        
        artistview.add(artist_grid)
    
    def getAlbums(self):
        albumview = self.ui.album_list
        
        for c in albumview.get_children():
            albumview.remove(c)
        
        while True:
            albumlist = self.controls.GetAlbums(self.artistid)
            if albumlist['type'] == 'response':
                break
        albums = albumlist['data']['albums']
        
        album_grid = DictionaryGrid(albums, keys=['label'])
        album_grid.columns['label'].set_title('Album')
        album_grid.connect('selection_changed', self.newAlbum)
        album_grid.show()
        
        albumview.add(album_grid)
    
    def getSongs(self):
        songview = self.ui.song_list
        
        for c in songview.get_children():
            songview.remove(c)

        while True:
            songlist = self.controls.GetSongs(self.artistid, self.albumid)
            if songlist['type'] == 'response':
                break
        songs = songlist['data']['songs']
        
        song_grid = DictionaryGrid(songs, keys=['label'])
        song_grid.columns['label'].set_title('Title')
        song_grid.connect('selection_changed', self.newSong)
        song_grid.show()
        
        songview.add(song_grid)
    
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
        if action['data'] == 'PlaybackResumed' or action['data'] == 'PlaybackStarted':
            self.playing = True
            self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
        elif action['data'] == 'PlaybackPaused':
            self.playing = True
            self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            
            
