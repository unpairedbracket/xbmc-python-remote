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
Provides JSON strings ready to be sent to XBMC Dharma. JsonBuilder is used to
generate the strings, and convenience methods are available to build requests
needed by Xbmcremote.
'''

from JsonBuilder import JsonBuilder

class JsonRpc(object):

    '''
    API implementation and convenience methods for XBMC Dharma

    Due to Dharma's incomplete and largely broken API, many things I would
    like to do aren't possible. I've still implemented conveniene methods for
    things that arent possible because they are implemented in Eden and beyond
    and exceptions would be thrown if the methods were not found.
    '''

    # API Namespaces
    AudioLibrary = JsonBuilder('AudioLibrary')
    AudioPlayer = JsonBuilder('AudioPlayer')
    Files = JsonBuilder('Files')
    JSONRPC = JsonBuilder('JSONRPC')
    Player = JsonBuilder('Player')
    Playlist = JsonBuilder('Playlist')
    AudioPlaylist = JsonBuilder('AudioPlaylist')
    VideoPlaylist = JsonBuilder('VideoPlaylist')
    PicturePlayer = JsonBuilder('PicturePlayer')
    System = JsonBuilder('System')
    VideoLibrary = JsonBuilder('VideoLibrary')
    VideoPlayer = JsonBuilder('VideoPlayer')
    XBMC = JsonBuilder('XBMC')
    # Special custom Namespace
    Custom = JsonBuilder()

    def start(self):
        '''Start playing the music playlist'''
        return self.AudioPlaylist.Play(identifier="control")

    def stop(self):
        '''Stop the music player'''
        return self.AudioPlayer.Stop(identifier="control")

    def play(self):
        '''Play or pause the music player'''
        return self.AudioPlayer.PlayPause(identifier="control")

    def next(self):
        '''Skip to the next item of the music playlist'''
        return self.AudioPlayer.SkipNext(identifier="control")

    def prev(self):
        '''Skip to the previous item of the music playlist'''
        return self.AudioPlayer.SkipPrevious(identifier="control")

    def state(self):
        '''Find out the state of the music player'''
        return self.AudioPlayer.State(identifier="state")

    def get_artists(self):
        '''Request the list of artists'''
        return self.AudioLibrary.GetArtists(identifier="artist_list")

    def get_albums(self, artistid=-1):
        '''Request the list of artists'''
        return self.AudioLibrary.GetAlbums(artistid=artistid,
                                      identifier="album_list")

    def get_songs(self, artistid=-1, albumid=-1):
        '''Request the list of songs'''
        return self.AudioLibrary.GetSongs(artistid=artistid,
                                     albumid=albumid,
                                     identifier="song_list")

    def get_players(self):
        '''Request the active players'''
        return self.Player.GetActivePlayers()


    def insert_song(self, songid, position=0):
        '''
        This isn't implemented in Dharma's broken API, but I need a method
        so things higher up don't throw exceptions when they try to call it.
        '''
        pass

    def insert_and_play(self, songid, position=0):
        '''
        This isn't implemented in Dharma's broken API, but I need a method
        so things higher up don't throw exceptions when they try to call it.
        '''
        pass

    def queue_song(self, songid):
        '''
        This isn't implemented in Dharma's broken API, but I need a method
        so things higher up don't throw exceptions when they try to call it.
        '''
        pass

    def get_position(self, identifier):
        '''
        This isn't implemented in Dharma's broken API, but I need a method
        so things higher up don't throw exceptions when they try to call it.
        '''
        pass

    def get_now_playing(self, playerid=0):
        '''
        This isn't implemented in Dharma's broken API, but I need a method
        so things higher up don't throw exceptions when they try to call it.
        '''
        pass

    def custom_method(self, method_name, params, identifier):
        '''create JSON strings for custom methods'''
        return self.Custom(method_name, identifier=identifier, **params)
