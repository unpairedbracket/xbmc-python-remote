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
        
        #sound menu integration
        self.sound_menu = SoundMenuControls('xbmcremote')
        self.sound_menu._sound_menu_next = self.nextSong
        self.sound_menu._sound_menu_previous = self.prevSong
        self.sound_menu._sound_menu_pause = self.sound_menu._sound_menu_play = self.play     
        self.sound_menu._sound_menu_is_playing = self.isPlaying   
        self.sound_menu._sound_menu_raise = self.show
        
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
            self.playerstate = self.controls.checkState()
            if self.playerstate['type'] != 'response':
                pass
            elif self.playerstate['data']['paused'] == False:
                self.playing = True
                self.paused = False
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
            elif self.playerstate['data']['paused'] == True:
                self.playing = True
                self.paused = True
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            else:
                self.playing = False
                self.paused = True
                self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            return True
        finally:
            return True
    
    def isPlaying(self):
        try:
            self.paused
        except AttributeError:
            self.paused = False
        return not self.paused 
    
    def getArtists(self):
        artistview = self.ui.artist_list
        
        while True:
            artistlist = self.controls.GetArtists()
            if artistlist['type'] == 'response':
                break
        artists = sorted(artistlist['data']['artists'], key = lambda k: k['label'])
        artists.insert(0, {'artistid': -1, 'label': '[All Artists]'})
        artist_grid = DictionaryGrid(artists, keys=['label'])
        
        artist_grid.columns['label'].set_title('Artists')
        artist_grid.set_headers_clickable(False)
        
        artist_grid.connect('selection_changed', self.threadNewArtist)
        artist_grid.show()
        
        for c in artistview.get_children():
            artistview.remove(c)
        
        artistview.add(artist_grid)
    
    def getAlbums(self):
        albumview = self.ui.album_list
        
        while True:
            albumlist = self.controls.GetAlbums(self.artistid)
            if albumlist['type'] == 'response':
                break
        albums = sorted(albumlist['data']['albums'], key = lambda k: k['label'])
        albums.insert(0, {'albumid': -1, 'label': '[All Albums]'})        
        album_grid = DictionaryGrid(albums, keys=['label'])
        
        album_grid.columns['label'].set_title('Albums')
        album_grid.set_headers_clickable(False)
        
        album_grid.connect('selection_changed', self.threadNewAlbum)
        album_grid.show()
        
        for c in albumview.get_children():
            albumview.remove(c)
        
        albumview.add(album_grid)
    
    def getSongs(self):
        songview = self.ui.song_list

        while True:
            songlist = self.controls.GetSongs(self.artistid, self.albumid)
            if songlist['type'] == 'response':
                break
        songs = sorted(songlist['data']['songs'], key = lambda k: k['label'])
        songs.insert(0, {'songid': -1, 'label': '[All Songs]'})
        song_grid = DictionaryGrid(songs, keys=['label'])
        
        song_grid.columns['label'].set_title('Songs')
        song_grid.set_headers_clickable(False)
        
        song_grid.connect('selection_changed', self.threadNewSong)
        song_grid.show() 
        
        for c in songview.get_children():
            songview.remove(c)
            
        songview.add(song_grid)
    
    def newArtist(self, widget, data=None):
        self.artistid = data[0]['artistid']
        self.albumid = -1
        self.getAlbums()
        self.getSongs()
        
    def threadNewArtist(self, widget, data=None):
        Thread(target=self.newArtist, args=(widget, data)).start()

    def newAlbum(self, widget, data=None):
        self.albumid = data[0]['albumid']
        self.getSongs()

    def threadNewAlbum(self, widget, data=None):
        Thread(target=self.newAlbum, args=(widget, data)).start()

    def newSong(self, widget, data=None):
        self.songid = data[0]['songid']

    def threadNewSong(self, widget, data=None):
        Thread(target=self.newSong, args=(widget, data)).start()
        
    def play(self):
        self.on_playback_play_clicked(None, None)

    def on_playback_play_clicked(self, widget, data=None):
        if not self.playing:
            response = self.controls.StartPlaying()
            self.sound_menu.song_changed()
        else:
            response = self.controls.PlayPause()
        self.actOnAction(response)
        
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
        Thread(target=self.updateLibrary).start()

    def on_xbmcremote_window_destroy(self, widget, data=None):
        self.controls.closeSocket()

    def actOnAction(self, action):
        if action['data'] == 'PlaybackResumed' or action['data'] == 'PlaybackStarted':
            self.playing = True
            self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PAUSE)
            self.sound_menu.signal_playing()
        elif action['data'] == 'PlaybackPaused':
            self.playing = True
            self.ui.playback_play.set_stock_id(gtk.STOCK_MEDIA_PLAY)
            self.sound_menu.signal_paused()
            
