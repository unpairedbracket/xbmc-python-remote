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

XBMC_START = buildJson("AudioPlaylist.Play")
XBMC_STOP = buildJson("AudioPlayer.Stop")
XBMC_PLAY = buildJson("AudioPlayer.PlayPause")
XBMC_NEXT = buildJson("AudioPlayer.SkipNext")
XBMC_PREV = buildJson("AudioPlayer.SkipPrevious")
    
def decodeAnnouncement(Json):
    #check last first to return the latest valid Announcement message
    for i in reversed(Json):
        js = decoder.decode(i)
        #check for a valid Announcement
        if js.get(u'method') == u'Announcement':
            message = js.get(u'params').get(u'message')
            return message

def decodeResponse(Json):
    #check last first to return the latest valid result
    for i in reversed(Json):
        js = decoder.decode(i)
        #check for a valid response
        if js.has_key(u'id'):
            result = js.get(u'result')
            return result
            
                