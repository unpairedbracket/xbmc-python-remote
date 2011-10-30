'''
Created on Aug 16, 2011

@author: benspiers
'''

import json

encoder = json.JSONEncoder()

def buildJson(method, params={}, identifier=1):
    jsonstring = {"jsonrpc": "2.0", "method": method, "params": params, "id": identifier}
    return encoder.encode(jsonstring)

#Control
XBMC_START = buildJson("AudioPlaylist.Play")
XBMC_STOP = buildJson("AudioPlayer.Stop")
XBMC_PLAY = buildJson("AudioPlayer.PlayPause")
XBMC_NEXT = buildJson("AudioPlayer.SkipNext")
XBMC_PREV = buildJson("AudioPlayer.SkipPrevious")
XBMC_STATE = buildJson("AudioPlayer.State")

#Library Requests
def GetArtists():
    return buildJson("AudioLibrary.GetArtists")

def GetAlbums(artistid=-1):
    params = {"artistid": artistid}
    return buildJson("AudioLibrary.GetAlbums", params)

def GetSongs(artistid=-1, albumid=-1):    
    params = {"artistid": artistid, "albumid": albumid}
    return buildJson("AudioLibrary.GetSongs", params)