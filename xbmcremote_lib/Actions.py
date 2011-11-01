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

import XBMCJsonObjects as XJ
from Sender import Sender
from Decoder import Decoder
from Queue import Queue
from threading import Thread

class Actions(object):

    def __init__(self, window):
        self.window = window
        self.send = Sender(self)
        self.queue = Queue()
        self.decoder = Decoder(self)
        self.start()
        
    def getSocket(self, IpAddress, Port):
        self.send.getSocket(IpAddress, Port) 

    def start(self):
        responder = Thread(target=self.worker, name='Response daemon')
        responder.daemon = True
        responder.start()
        
    def add(self, data):
        self.queue.put(data)
           
    def sendCallback(self, jsonlist, callback):
        json = '[' + jsonlist.replace('}\n{', '},{') + ']'
        self.decoder.decode(json, callback)
        
    def worker(self):
        while True:
            try:
                item = self.queue.get()
                kind = item['kind']
                data = item['data']
                callback = item['callback']
                #Show a nice error dialog or raise an exception
                if kind == 'error':
                    self.handle_error(data)
                #Use callbacks if the data is for something unconventional
                elif callback is not None:
                    callback(data)
                #Otherwise this will work out what to do with it
                elif kind == 'response':
                    if data.has_key('playing') and data.has_key('paused'):
                        self.window.actOnAction(data)
                    elif data.has_key('artists'):
                        self.window.updateArtistList(data)
                    elif data.has_key('albums'):
                        self.window.updateAlbumList(data)
                    elif data.has_key('songs'):
                        self.window.updateSongList(data)
                    else:
                        print data
                elif kind == 'announcement':
                    print data
                else:
                    print data

            except:
                #TODO Do something
                pass
    
    def handle_error(self, error):
        if self.window is None:
            raise RuntimeError(error)
        else:
            self.window.handle_error(error)
        
    def kill(self):
        self.send.closeSocket()

    def PlayPause(self):
        
        action = XJ.XBMC_PLAY
        self.send.add(action)
                
    def PlayNext(self):
        
        action = XJ.XBMC_NEXT
        self.send.add(action)
                
    def PlayPrevious(self):
        
        action = XJ.XBMC_PREV
        self.send.add(action)
                
    def StartPlaying(self):
        
        action = XJ.XBMC_START
        self.send.add(action)
                
    def StopPlaying(self):
        
        action = XJ.XBMC_STOP
        self.send.add(action)
    
    def CheckState(self):
        
        action = XJ.XBMC_STATE
        self.send.add(action)
                  
    def GetArtists(self):
        
        action = XJ.GetArtists()
        self.send.add(action, timeout=0.5)
            
    def GetAlbums(self, artistid=-1):
        
        action = XJ.GetAlbums(artistid)
        self.send.add(action, timeout=0.5)
    
    def GetSongs(self, artistid=-1, albumid=-1):
        
        action = XJ.GetSongs(artistid, albumid)
        self.send.add(action, timeout=0.5)
        
    def SendCustomRequest(self, method, params={}, callback=None, timeout=0.1):
        
        action = XJ.buildJson(method, params, 'custom')
        self.send.add(action, callback, timeout)
        
