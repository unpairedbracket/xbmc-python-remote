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

from xbmcremote_lib.DummyInterface import BaseInterface
from XbmcremoteWindow import XbmcremoteWindow
from quickly.widgets.dictionary_grid import DictionaryGrid
import gtk
import gobject

class WindowInterface(BaseInterface):
    
    def __init__(self, controller):
        self.controller = controller
        self.updating = False
        self.window = XbmcremoteWindow()
        self.methods = {'artist_list': self.updateArtistList,
                        'album_list': self.updateAlbumList,
                        'song_list': self.updateSongList, }
        self.window.set_interface(self)
        
    def refresh(self, try_connect=True):
        super(WindowInterface, self).refresh(try_connect)
        
        if self.controller.connected:
            gobject.idle_add(self.window.ui.connected_to.set_label, 'Connected to: '+self.controller.ip+':'+str(self.controller.port))
            self.updateLibrary()
            self.updatePlaying()
            if not self.updating:
                #gobject.timeout_add(1000, self.updatePlaying)
                self.updating = True
        else:
            gobject.idle_add(self.window.ui.connected_to.set_label, 'Connection Failed!')
    
    def show(self):
        self.window.show()
    
    def start_loop(self):
        gobject.threads_init()
        gtk.main()
        
    def updatePlaying(self):
        try:
            self.controller.CheckState()
        finally:
            return True
    
    def updateLibrary(self):
        self.controller.GetArtists()
        self.controller.GetAlbums()
        self.controller.GetSongs()
        
    def paused(self, paused):
        if paused:
            gobject.idle_add(self.window.ui.playback_play.set_stock_id, gtk.STOCK_MEDIA_PLAY)
        else:
            gobject.idle_add(self.window.ui.playback_play.set_stock_id, gtk.STOCK_MEDIA_PAUSE)

    def updateArtistList(self, artistlist):        
        artist_view = self.window.ui.artist_list
        
        artists = sorted(artistlist['artists'], key = lambda k: k['label'])
        artists.insert(0, {'artistid': -1, 'label': '[All Artists]'})
        artist_grid = DictionaryGrid(artists, keys=['label'])
        
        artist_grid.columns['label'].set_title('Artists')
        artist_grid.set_headers_clickable(False)
        
        artist_grid.connect('selection_changed', self.window.newArtist)
        gobject.idle_add(self.update_view, artist_view, artist_grid)
            
    def updateAlbumList(self, albumlist):        
        album_view = self.window.ui.album_list
            
        albums = sorted(albumlist['albums'], key = lambda k: k['label'])
        albums.insert(0, {'albumid': -1, 'label': '[All Albums]'})        
        album_grid = DictionaryGrid(albums, keys=['label'])
        
        album_grid.columns['label'].set_title('Albums')
        album_grid.set_headers_clickable(False)
        
        album_grid.connect('selection_changed', self.window.newAlbum)
        gobject.idle_add(self.update_view, album_view, album_grid)
               
    def updateSongList(self, songlist):        
        song_view = self.window.ui.song_list
             
        songs = sorted(songlist['songs'], key = lambda k: k['label'])
        songs.insert(0, {'songid': -1, 'label': '[All Songs]'})
        song_grid = DictionaryGrid(songs, keys=['label'])
        
        song_grid.columns['label'].set_title('Songs')
        song_grid.set_headers_clickable(False)
        
        song_grid.connect('selection_changed', self.window.newSong)
        gobject.idle_add(self.update_view, song_view, song_grid)
        
    def update_view(self, view, grid):
        grid.show()
        
        for c in view.get_children():
            view.remove(c)
        
        view.add(grid)



             
        