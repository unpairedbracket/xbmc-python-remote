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

from xbmcremote.interfaces import BaseInterface
from XbmcremoteWindow import XbmcremoteWindow
from quickly.widgets.dictionary_grid import DictionaryGrid
from gi.repository import Gtk
from gi.repository import GObject

class GtkInterface(BaseInterface):

    def __init__(self, application):
        BaseInterface.__init__(self, application)
        self.window = XbmcremoteWindow()
        self.methods = {'artist_list': self.updateArtistList,
                        'album_list': self.updateAlbumList,
                        'song_list': self.updateSongList, 
                        'now_playing': self.update_now_playing}
        self.window.set_interface(self)

    def refresh(self, signaller, data=None):
        GObject.idle_add(self.window.ui.connected_to.set_label, 'Connected to: '+self.state['ip']+':'+str(self.state['port']))
        self.updatePlaying()
        self.updateLibrary()

    def disconnected(self, signaller, data=None):
        GObject.idle_add(self.window.ui.connected_to.set_label, 'Connection Failed')

    def show(self):
        self.window.show()

    def start_loop(self):
        self.connect('xbmc_connected', self.refresh)
        self.connect("xbmc_new_playing", self.update_now_playing)
        self.show()
        self.refresh(None)
        Gtk.main()

    def updatePlaying(self):
        try:
            self.emit("xbmc_get", "state", None)
            self.emit("xbmc_get", "now_playing", None)
        finally:
            return True

    def updateLibrary(self):
        self.emit("xbmc_get", "artists", None)
        self.emit("xbmc_get", "albums", None)
        self.emit("xbmc_get", "songs", None)

    def paused(self, signaller, paused, data=None):
        if paused:
            GObject.idle_add(self.window.ui.playback_play.set_stock_id, Gtk.STOCK_MEDIA_PLAY)
        else:
            GObject.idle_add(self.window.ui.playback_play.set_stock_id, Gtk.STOCK_MEDIA_PAUSE)

    def updateArtistList(self, artistlist):
        artist_view = self.window.ui.artist_list

        artists = sorted(artistlist['artists'], key = lambda k: k['label'])
        artists.insert(0, {'artistid': -1, 'label': '[All Artists]'})
        artist_grid = DictionaryGrid(artists, keys=['label'])

        artist_grid.columns['label'].set_title('Artists')
        artist_grid.set_headers_clickable(False)

        artist_grid.connect('selection_changed', self.window.newArtist)
        GObject.idle_add(self.update_view, artist_view, artist_grid)

    def updateAlbumList(self, albumlist):
        album_view = self.window.ui.album_list

        albums = sorted(albumlist['albums'], key = lambda k: k['label'])
        albums.insert(0, {'albumid': -1, 'label': '[All Albums]'})
        album_grid = DictionaryGrid(albums, keys=['label'])

        album_grid.columns['label'].set_title('Albums')
        album_grid.set_headers_clickable(False)

        album_grid.connect('selection_changed', self.window.newAlbum)
        GObject.idle_add(self.update_view, album_view, album_grid)

    def updateSongList(self, songlist):
        song_view = self.window.ui.song_list

        songs = sorted(songlist['songs'], key = lambda k: k['label'])
        songs.insert(0, {'songid': -1, 'label': '[All Songs]'})
        song_grid = DictionaryGrid(songs, keys=['label'])

        song_grid.columns['label'].set_title('Songs')
        song_grid.set_headers_clickable(False)

        song_grid.connect('selection_changed', self.window.newSong)
        GObject.idle_add(self.update_view, song_view, song_grid)

    def update_view(self, view, grid):
        grid.show()

        for c in view.get_children():
            view.remove(c)

        view.add(grid)

    def update_now_playing(self, signaller, artist, album, title, data=None):
        GObject.idle_add(self.window.ui.now_playing_label.set_label, ' '.join([title, 'by', artist, 'from', album]))

    def handle_error(self, signaller, message, code, identifier, data=None):
        if identifier == 'now_playing' and code == -32100:
            GObject.idle_add(self.window.ui.now_playing_label.set_label, 'Not Playing')
        elif self.window.ErrorDialog is not None:
            error_dialog = self.window.ErrorDialog()
            error_dialog.set_error(message, code, identifier)
            GObject.idle_add(error_dialog.show)



