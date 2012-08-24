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

import json

encoder = json.JSONEncoder()

def buildJson(method, params={}, identifier=1):
    jsonstring = {"jsonrpc": "2.0", "method": method, "params": params, "id": identifier}
    return encoder.encode(jsonstring)

#Control
XBMC_START = buildJson("AudioPlaylist.Play", identifier="control")
XBMC_STOP = buildJson("AudioPlayer.Stop", identifier="control")
XBMC_PLAY = buildJson("AudioPlayer.PlayPause", identifier="control")
XBMC_NEXT = buildJson("AudioPlayer.SkipNext", identifier="control")
XBMC_PREV = buildJson("AudioPlayer.SkipPrevious", identifier="control")
XBMC_STATE = buildJson("AudioPlayer.State", identifier="state")

#Library Requests
def GetArtists():
    return buildJson("AudioLibrary.GetArtists", identifier="artist_list")

def GetAlbums(artistid=-1):
    params = {"artistid": artistid}
    return buildJson("AudioLibrary.GetAlbums", params, identifier="album_list")

def GetSongs(artistid=-1, albumid=-1):
    params = {"artistid": artistid, "albumid": albumid}
    return buildJson("AudioLibrary.GetSongs", params, identifier="song_list")
