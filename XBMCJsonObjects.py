'''
Created on Aug 16, 2011

@author: benspiers
'''

class XBMCJson(object):
    
    def __init__(self):
        self.XBMC_START = self.buildJson("AudioPlaylist.Play")
        self.XBMC_STOP = self.buildJson("AudioPlayer.Stop")
        self.XBMC_PLAY = self.buildJson("AudioPlayer.PlayPause")
        self.XBMC_NEXT = self.buildJson("AudioPlayer.SkipNext")
        self.XBMC_PREV = self.buildJson("AudioPlayer.SkipPrevious")

    def buildJson(self, method, params={}, identifier=1):
        import json
        encoder = json.JSONEncoder()
        jsonstring = {"jsonrpc": "2.0", "method": method, "params": params, "id": identifier}
        return encoder.encode(jsonstring)
