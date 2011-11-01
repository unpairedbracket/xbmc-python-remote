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

from xbmcremote_lib import Window
from xbmcremote_lib.Actions import Actions
from xbmcremote_lib.preferences import preferences
from xbmcremote_lib.sound_menu import SoundMenuControls
from xbmcremote.AboutXbmcremoteDialog import AboutXbmcremoteDialog
from xbmcremote.PreferencesXbmcremoteDialog import PreferencesXbmcremoteDialog
from xbmcremote.ErrorDialog import ErrorDialog

from threading import Thread
import socket

# See xbmcremote_lib.Window.py for more details about how this class works
class XbmcremoteWindow(Window):
    __gtype_name__ = 'XbmcremoteWindow'

    def finish_initializing(self, builder): # pylint: disable=E1002
        '''Set up the main window'''
        super(XbmcremoteWindow, self).finish_initializing(builder)
        self.controls = Actions(self)
        self.AboutDialog = AboutXbmcremoteDialog
        self.PreferencesDialog = PreferencesXbmcremoteDialog
        self.ErrorDialog = ErrorDialog
        
        # Code for other initialization actions should be added here.
        # Make my threads work
        gobject.threads_init()
        
        self.playing = self.paused = False
        self.artistid = self.albumid = self.songid = -1
        self.ip = preferences['ip_entry']
        self.port = int(preferences['port_entry'])
        
        self.connect_to_xbmc()
        if self.connected:
            self.updateLibrary()
            self.updatePlaying()
            gobject.timeout_add(1000, self.updatePlaying)

        #sound menu integration
        self.sound_menu = SoundMenuControls('xbmcremote')
        self.sound_menu._sound_menu_next = self.nextSong
        self.sound_menu._sound_menu_previous = self.prevSong
        self.sound_menu._sound_menu_pause = self.sound_menu._sound_menu_play = self.play     
        self.sound_menu._sound_menu_is_playing = self.isPlaying   
        self.sound_menu._sound_menu_raise = self.show
        
    def connect_to_xbmc(self):
        address_label = self.ui.connected_to
        try:
            self.controls.getSocket(self.ip, self.port)
            address_label.set_label('Connected to: '+self.ip+':'+str(self.port))
            self.connected = True
        except socket.error:
            address_label.set_label('Connection Failed!')
            self.connected = False
             
    def updateLibrary(self):
        self.controls.GetArtists()
        self.controls.GetAlbums()
        self.controls.GetSongs()
    
    def updatePlaying(self):
        try:
            self.controls.CheckState()
        finally:
            return True
    
    def isPlaying(self):
        return not self.paused
    
    def updateArtistList(self, artistlist):        
        artistview = self.ui.artist_list
        
        artists = sorted(artistlist['artists'], key = lambda k: k['label'])
        artists.insert(0, {'artistid': -1, 'label': '[All Artists]'})
        artist_grid = DictionaryGrid(artists, keys=['label'])
        
        artist_grid.columns['label'].set_title('Artists')
        artist_grid.set_headers_clickable(False)
        
        artist_grid.connect('selection_changed', self.newArtist)
        artist_grid.show()
        
        for c in artistview.get_children():
            artistview.remove(c)
        
        artistview.add(artist_grid)
            
    def updateAlbumList(self, albumlist):        
        albumview = self.ui.album_list
            
        albums = sorted(albumlist['albums'], key = lambda k: k['label'])
        albums.insert(0, {'albumid': -1, 'label': '[All Albums]'})        
        album_grid = DictionaryGrid(albums, keys=['label'])
        
        album_grid.columns['label'].set_title('Albums')
        album_grid.set_headers_clickable(False)
        
        album_grid.connect('selection_changed', self.newAlbum)
        album_grid.show()
        
        for c in albumview.get_children():
            albumview.remove(c)
        
        albumview.add(album_grid)
               
    def updateSongList(self, songlist):        
        songview = self.ui.song_list
             
        songs = sorted(songlist['songs'], key = lambda k: k['label'])
        songs.insert(0, {'songid': -1, 'label': '[All Songs]'})
        song_grid = DictionaryGrid(songs, keys=['label'])
        
        song_grid.columns['label'].set_title('Songs')
        song_grid.set_headers_clickable(False)
        
        song_grid.connect('selection_changed', self.newSong)
        song_grid.show() 
        
        for c in songview.get_children():
            songview.remove(c)
            
        songview.add(song_grid)
    
    def newArtist(self, widget, data=None):
        self.artistid = data[0]['artistid']
        self.albumid = -1
        self.controls.GetAlbums(self.artistid)
        self.controls.GetSongs(self.artistid, self.albumid)
        
    def newAlbum(self, widget, data=None):
        self.albumid = data[0]['albumid']
        self.controls.GetSongs(self.artistid, self.albumid)

    def newSong(self, widget, data=None):
        self.songid = data[0]['songid']

    def play(self):
        self.on_playback_play_clicked(None, None)

    def on_playback_play_clicked(self, widget, data=None):
        if not self.playing:
            self.controls.StartPlaying()
            self.sound_menu.song_changed()
        else:
            self.controls.PlayPause()
        
    def nextSong(self):
        self.on_playback_next_clicked(None, None)

    def on_playback_next_clicked(self, widget, data=None):
        self.controls.PlayNext()
        self.sound_menu.song_changed()
        
    def prevSong(self):
        self.on_playback_previous_clicked(None, None)

    def on_playback_previous_clicked(self, widget, data=None):
        self.controls.PlayPrevious()
        self.sound_menu.song_changed()

    def on_refresh_clicked(self, widget, data=None):
        if self.connected:
            self.updateLibrary()

    def on_xbmcremote_window_destroy(self, widget, data=None):
        if self.connected:
            self.controls.kill()

    def actOnAction(self, data):
        if data.has_key('playing') and data.has_key('paused'):
            self.playing = data['playing']
            self.paused = data['paused']
            if data['paused']:
                self.sound_menu.signal_paused()
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            else:
                self.sound_menu.signal_playing()
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
            
    def handle_error(self, error):
        """Display the error box."""
        if self.ErrorDialog is not None:
            error_dialog = self.ErrorDialog(error['message'])
            error_dialog.show()

            
