'''
Created on Aug 16, 2011

@author: benspiers
'''

import json

encoder = json.JSONEncoder()
decoder = json.JSONDecoder()

def buildJson(method, params={}, identifier=1):
    jsonstring = {"jsonrpc": "2.0", "method": method, "params": params, "id": identifier}
    return encoder.encode(jsonstring)
#Control
XBMC_START = buildJson("AudioPlaylist.Play")
XBMC_STOP = buildJson("AudioPlayer.Stop")
XBMC_PLAY = buildJson("AudioPlayer.PlayPause")
XBMC_NEXT = buildJson("AudioPlayer.SkipNext")
XBMC_PREV = buildJson("AudioPlayer.SkipPrevious")

#Library Requests
def GetArtists():
    return buildJson("AudioLibrary.GetArtists")

def GetAlbums(artistid=-1):
    
    params = {"artistid": artistid}
    return buildJson("AudioLibrary.GetAlbums", params)

def GetSongs(artistid=-1, albumid=-1):
    
    params = {"artistid": artistid, "albumid": albumid}
    return buildJson("AudioLibrary.GetSongs", params)

# TODO: improve decoding
def decodeAnnouncement(Json):
    #check last first to return the latest valid Announcement message
    for i in reversed(Json):
        try:
            js = decoder.decode(i)
            #check for a valid Announcement
            if js['method'] == 'Announcement':
                message = js['params']['message']
                return {'type': 'announcement', 'data': message}
        except (ValueError, KeyError):
            pass
    return decodeError(Json)

def decodeResponse(Json):
    #check last first to return the latest valid result
    for i in reversed(Json):
        try:
            js = decoder.decode(i)
            #check for a valid response
            if js.has_key(u'error'):
                break
            if js.has_key(u'id'):
                result = js['result']
                return {'type': 'response', 'data': result}
        except ValueError:
            pass
    return decodeError(Json)

def decodeError(Json):
    
    for i in reversed(Json):
        try:
            js = decoder.decode(i)
            #check for an error
            if js.has_key(u'error'):
                result = js['error']
                return {'type': 'error', 'data': result}
        except ValueError:
            pass
    #if nothing found, return empty dictionary
    return {'type': 'none', 'data': {}}
