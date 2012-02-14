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

import json

encoder = json.JSONEncoder()

def buildJson(method, params={}, identifier=1):
    jsonstring = {"jsonrpc": "2.0", "method": method, "params": params, "id": identifier}
    return encoder.encode(jsonstring)

#Control
XBMC_START = buildJson("Playlist.Play", {'playerid':0})
XBMC_STOP = buildJson("Player.Stop", {'playerid': 0})
XBMC_PLAY = buildJson("Player.PlayPause", {'playerid': 0})
XBMC_NEXT = buildJson("Player.GoNext", {'playerid': 0})
XBMC_PREV = buildJson("Player.GoPrevious", {'playerid': 0})
XBMC_STATE = buildJson("Player.GetProperties", {'playerid': 0, 'properties': ['speed', 'partymode', 'shuffled', 'repeat', 'playlistid']})

#Library Requests
def GetArtists():
    return buildJson("AudioLibrary.GetArtists")

def GetAlbums(artistid=-1):
    params = {}
    if artistid != -1:
        params['artistid'] = artistid
    return buildJson("AudioLibrary.GetAlbums", params)

def GetSongs(artistid=-1, albumid=-1):
    params = {}
    if artistid != -1:
        params['artistid'] = artistid
    if albumid != -1:
        params['albumid'] = albumid
    return buildJson("AudioLibrary.GetSongs", params)