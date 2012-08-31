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
Module contains GtkFrontend class.
'''

from ast import literal_eval
from xbmcremote.frontends import BaseFrontend
from XbmcremoteWindow import XbmcremoteWindow
from quickly.widgets.dictionary_grid import DictionaryGrid
from gi.repository import Gtk, GObject


class GtkFrontend(BaseFrontend):
    '''Frontend using the gtk widget toolkit'''

    def __init__(self, application):
        BaseFrontend.__init__(self, application)
        self.window = XbmcremoteWindow()
        self.methods = {'artist_list': self.update_artist_list,
                        'album_list': self.update_album_list,
                        'song_list': self.update_song_list,
                        'now_playing': self.update_now_playing}
        self.window.set_frontend(self)
        self.set_connection_label = self.window.ui.connected_to.set_label
        self.set_playing_label = self.window.ui.now_playing_label.set_label
        self.set_play_button = self.window.ui.playback_play.set_stock_id
        GObject.threads_init()

    def refresh(self, signaller, data=None):
        '''
        Called by xbmc_reconnected signal when a connection is established
        or by the refresh button in XbmcRemoteWindow
        '''
        connection = ''.join(['Connected to: ', self.state['ip'],
                              ':', str(self.state['port'])])
        GObject.idle_add(self.set_connection_label, connection)
        for signal in ('state', 'now_playing', 'artists', 'albums', 'songs'):
            self.emit("xbmc_control", signal, None)

    def disconnected(self, signaller, data=None):
        '''Update the window to show that a connection has failed'''
        GObject.idle_add(self.set_connection_label, 'Connection Failed')

    def start_loop(self):
        '''Connect signals, show the window and start the mainloop'''
        self.signal_connect('xbmc_connected', self.refresh)
        self.signal_connect('xbmc_disconnected', self.disconnected)
        self.window.show()
        if self.state['connected']:
            self.refresh(None)
        else:
            self.emit('xbmc_reconnect')
        Gtk.main()

    def paused(self, signaller, paused, data=None):
        if paused:
            GObject.idle_add(self.set_play_button, Gtk.STOCK_MEDIA_PLAY)
        else:
            GObject.idle_add(self.set_play_button, Gtk.STOCK_MEDIA_PAUSE)

    @staticmethod
    def update_list(response, kind):
        '''Return a DictionaryGrid with the sorted response in it'''
        plural = ''.join([kind, 's'])
        label = ''.join(['[All ', plural.capitalize(), ']'])
        kind_id = ''.join([kind, 'id'])
        items = sorted(response[plural], key=lambda k: k['label'])
        items.insert(0, {kind_id: -1, 'label': label})
        grid = DictionaryGrid(items, keys=['label'])
        title = plural.capitalize()
        grid.columns['label'].set_title(title)
        grid.set_headers_clickable(False)
        return grid

    def update_artist_list(self, artist_list):
        '''Prepare objects to update the artist list'''
        artist_grid = self.update_list(artist_list, 'artist')
        artist_view = self.window.ui.artist_list

        artist_grid.connect('selection_changed', self.window.new_artist)
        GObject.idle_add(self.__prepare_view, artist_view, artist_grid)

    def update_album_list(self, album_list):
        '''Prepare objects to update the album list'''
        album_grid = self.update_list(album_list, 'album')
        album_view = self.window.ui.album_list

        album_grid.connect('selection_changed', self.window.new_album)
        GObject.idle_add(self.__prepare_view, album_view, album_grid)

    def update_song_list(self, song_list):
        '''Prepare objects to update the song list'''
        song_grid = self.update_list(song_list, 'song')
        song_view = self.window.ui.song_list

        song_grid.connect('selection_changed', self.window.new_song)
        GObject.idle_add(self.__prepare_view, song_view, song_grid)

    @staticmethod
    def __prepare_view(view, grid):
        '''Put grid into view. Only call using GObject.idle_add().'''
        grid.show()

        for child in view.get_children():
            view.remove(child)

        view.add(grid)

    def update_now_playing(self, song_info):
        '''Change the now playing label to keep it up to date.'''
        now_playing = ' '.join([song_info['item']['title'], 'by',
                                song_info['item']['artist'], 'from',
                                song_info['item']['album']])
        GObject.idle_add(self.set_playing_label, now_playing)

    def handle_error(self, signaller, error, data=None):
        '''Catch and handle known errors or open a dialog.'''
        error = literal_eval(error)
        message = error['data']['message']
        code = error['data']['code']
        identifier = error['id']
        if identifier == 'now_playing' and code == -32100:
            GObject.idle_add(self.window.ui.now_playing_label.set_label,
                             'Not Playing')
        elif self.window.ErrorDialog is not None:
            error_dialog = self.window.ErrorDialog()
            error_dialog.set_error(message, code, identifier)
            GObject.idle_add(error_dialog.show)
