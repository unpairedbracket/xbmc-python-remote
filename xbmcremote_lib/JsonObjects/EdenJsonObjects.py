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

from JsonBuilder import JsonBuilder

class ProperJson(object):

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

    Custom = JsonBuilder()

JsonRpc = ProperJson()

#Control
XBMC_GET_PLAYERS = JsonRpc.Playlist.GetPlayers
XBMC_START = JsonRpc.Playlist.Play(playerid=0)
XBMC_STOP = JsonRpc.Player.Stop(playerid=0)
XBMC_PLAY = JsonRpc.Player.PlayPause(playerid=0)
XBMC_NEXT = JsonRpc.Player.GoNext(playerid=0)
XBMC_PREV = JsonRpc.Player.GoPrevious(playerid=0)
XBMC_STATE =JsonRpc.Player.GetProperties(playerid=0, properties=['speed', 'partymode', 'shuffled', 'repeat', 'playlistid'], identifier='state')

#Library Requests
def GetArtists():
    return JsonRpc.AudioLibrary.GetArtists(identifier='artist_list')

def GetAlbums(artistid=-1):
    if artistid == -1:
        return JsonRpc.AudioLibrary.GetAlbums(identifier='album_list')
    else:
        return JsonRpc.AudioLibrary.GetAlbums(artistid=artistid, identifier='album_list')

def GetSongs(artistid=-1, albumid=-1):
    if artistid == -1 and albumid == -1:
        return JsonRpc.AudioLibrary.GetSongs(identifier='song_list')
    elif albumid == -1:
        return JsonRpc.AudioLibrary.GetSongs(artistid=artistid, identifier='song_list')
    elif artistid == -1:
        return JsonRpc.AudioLibrary.GetSongs(albumid=albumid, identifier='song_list')
    else:
        return JsonRpc.AudioLibrary.GetSongs(artistid=artistid, albumid=albumid, identifier='song_list')

def GetPlayers():
    return JsonRpc.Player.GetPlayers

def GetNowPlaying(playerid=0):
    return JsonRpc.Player.GetItem(playerid=playerid, properties=['title','artist','album'], identifier='now_playing')

''' Here are all the JSON methods there are
Application.GetProperties
Application.Quit
Application.SetMute
Application.SetVolume

AudioLibrary.Clean
AudioLibrary.Export
AudioLibrary.GetAlbumDetails
AudioLibrary.GetAlbums
AudioLibrary.GetArtistDetails
AudioLibrary.GetArtists
AudioLibrary.GetGenres
AudioLibrary.GetRecentlyAddedAlbums
AudioLibrary.GetRecentlyAddedSongs
AudioLibrary.GetSongDetails
AudioLibrary.GetSongs
AudioLibrary.Scan

Files.Download
Files.GetDirectory
Files.GetSources

Input.Back
Input.Down
Input.Home
Input.Left
Input.Right
Input.Select
Input.Up

JSONRPC.Introspect
JSONRPC.NotifyAll
JSONRPC.Permission
JSONRPC.Ping
JSONRPC.Version

Player.GetActivePlayers
Player.GetItem
Player.GetProperties
Player.GoNext
Player.GoPrevious
Player.GoTo
Player.MoveDown
Player.MoveLeft
Player.MoveRight
Player.MoveUp
Player.Open
Player.PlayPause
Player.Repeat
Player.Rotate
Player.Seek
Player.SetAudioStream
Player.SetSpeed
Player.SetSubtitle
Player.Shuffle
Player.Stop
Player.UnShuffle
Player.Zoom
Player.ZoomIn
Player.ZoomOut
Playlist.Add
Playlist.Clear
Playlist.GetItems
Playlist.GetPlaylists
Playlist.GetProperties
Playlist.Insert
Playlist.Remove
Playlist.Swap

System.GetProperties
System.Hibernate
System.Reboot
System.Shutdown
System.Suspend

VideoLibrary.Clean
VideoLibrary.Export
VideoLibrary.GetEpisodeDetails
VideoLibrary.GetEpisodes
VideoLibrary.GetGenres
VideoLibrary.GetMovieDetails
VideoLibrary.GetMovieSetDetails
VideoLibrary.GetMovieSets
VideoLibrary.GetMovies
VideoLibrary.GetMusicVideoDetails
VideoLibrary.GetMusicVideos
VideoLibrary.GetRecentlyAddedEpisodes
VideoLibrary.GetRecentlyAddedMovies
VideoLibrary.GetRecentlyAddedMusicVideos
VideoLibrary.GetSeasons
VideoLibrary.GetTVShowDetails
VideoLibrary.GetTVShows
VideoLibrary.Scan

XBMC.GetInfoBooleans
XBMC.GetInfoLabels

Look in XBMC's JSON-RPC APIv4 Documentation for details'''

