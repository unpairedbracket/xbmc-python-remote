# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Ben Spiers 
# 
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
Provides JSON strings ready to be sent to XBMC Frodo. JsonBuilder is used to
generate the strings, and convenience methods are available to build requests
needed by Xbmcremote.
'''

from JsonBuilder import JsonBuilder

class JsonRpc(object):

    '''
    API implementation and convenience methods for XBMC Frodo

    (Pre-)Frodo has some API differences that break compatibility with Eden.
    '''

    # API Namespaces
    Application = JsonBuilder('Application')
    AudioLibrary = JsonBuilder('AudioLibrary')
    Files = JsonBuilder('Files')
    Input = JsonBuilder('Input')
    JSONRPC = JsonBuilder('JSONRPC')
    Player = JsonBuilder('Player')
    Playlist = JsonBuilder('Playlist')
    System = JsonBuilder('System')
    VideoLibrary = JsonBuilder('VideoLibrary')
    XBMC = JsonBuilder('XBMC')
    # Special custom Namespace
    Custom = JsonBuilder()

    def start(self):
        '''Start playing the music playlist'''
        return self.Player.Open(item={'playlistid': 0})

    def stop(self):
        '''Stop the music player'''
        return self.Player.Stop(playerid=0)

    def play(self):
        '''Play or pause the music player'''
        return self.Player.PlayPause(playerid=0)

    def next(self):
        '''Skip to the next item of the music playlist'''
        return self.Player.GoTo(playerid=0, to='next')

    def prev(self):
        '''Skip to the previous item of the music playlist'''
        return self.Player.GoTo(playerid=0, to='previous')

    def state(self):
        '''Find out the state of the music player'''
        properties = ['speed', 'partymode', 'shuffled', 'repeat', 'playlistid']
        return self.Player.GetProperties(playerid=0, properties=properties,
                                         identifier='state')

    def get_artists(self):
        '''Request the list of artists'''
        return self.AudioLibrary.GetArtists(identifier='artist_list')

    def get_albums(self, artistid=-1):
        '''Request the list of artists'''
        if artistid != -1:
            params = {'artistid': artistid}
            return self.AudioLibrary.GetAlbums(identifier='album_list',
                                               filter=params)
        else:
            return self.AudioLibrary.GetAlbums(identifier='album_list')

    def get_songs(self, artistid=-1, albumid=-1):
        '''Request the list of songs'''
        params = {}
        if artistid != -1:
            params['artistid'] = artistid
        if albumid != -1 :
            params['albumid'] = albumid
        if params != {}:
            return self.AudioLibrary.GetSongs(identifier='song_list',
                                              filter=params)
        else:
            return self.AudioLibrary.GetSongs(identifier='song_list')

    def get_players(self):
        '''Request the active players'''
        return self.Player.GetActivePlayers()

    def insert_song(self, songid, position=0):
        '''Insert songid into the music playlist at position'''
        return self.Playlist.Insert(playlistid=0, position=position, 
                                        item={'songid': songid})

    def insert_and_play(self, songid, position=0):
        '''Insert songid into the music playlist at position and play it'''
        insert =  self.insert_song(songid=songid, position=position)
        play = self.Player.GoTo(playerid=0, to=position)
        return ''.join(['[', insert, ',', play, ']'])

    def queue_song(self, songid):
        '''Add songid to the end of the music playlist'''
        return self.Playlist.Add(playlistid=0, item={'songid': songid})

    def get_position(self, identifier):
        '''Get the position of the currently playing item'''
        return self.Player.GetProperties(playerid=0, properties=['position'],
                                            identifier=identifier)

    def get_now_playing(self, playerid=0):
        '''Get the details of the currently playing item'''
        return self.Player.GetItem(
            playerid=playerid, properties=['title','artist','album'],
            identifier='now_playing'
        )

    def custom_method(self, method_name, params, identifier):
        '''Create JSON strings for custom methods'''
        return self.Custom(method_name, identifier=identifier, **params)

