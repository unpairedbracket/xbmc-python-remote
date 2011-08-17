'''
Created on Aug 16, 2011

@author: benspiers
'''

class XBMCJson(object):
    
    def __init__(self):
        import json
        jsonEncoder = json.JSONEncoder()
        self.XBMC_PLAY = jsonEncoder.encode({"jsonrpc": "2.0", "method": "AudioPlayer.PlayPause", "id": 1})
        self.XBMC_NEXT = jsonEncoder.encode({"jsonrpc": "2.0", "method": "AudioPlayer.SkipNext", "id": 1})
        self.XBMC_PREV = jsonEncoder.encode({"jsonrpc": "2.0", "method": "AudioPlayer.SkipPrevious", "id": 1})
