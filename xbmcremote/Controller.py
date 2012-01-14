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

from interfaces.WindowInterface import WindowInterface
from interfaces.TextInterface import TextInterface
from xbmcremote_lib import DharmaJsonObjects as XJ
from xbmcremote_lib.Sender import Sender
from xbmcremote_lib.Decoder import Decoder
from xbmcremote_lib.preferences import preferences
from xbmcremote_lib.sound_menu import SoundMenuControls
from Queue import Queue, Empty
from threading import Thread
from socket import error as SocketError


class Controller(object):
    
    def __init__(self, gui):
        
        self.gui = gui
        if self.gui:
            self.ui = WindowInterface(self)
        else:
            self.ui = TextInterface(self)
            
        self.sound_menu_integration = True
        self.connected = False
        self.queue = Queue()
        
        #Initialise parts
        self.send = Sender(self)
        self.decoder = Decoder(self)
        
        #Start program running with responder thread
        self.start_running()
        
        self.playing = self.paused = False

        #Server settings
        self.ip = preferences['ip_entry']
        self.port = int(preferences['port_entry'])
        
        if self.sound_menu_integration:
            self.integrate_sound_menu()
        
        self.ui.show()
        self.ui.refresh()
        self.ui.start_loop()
        
    def start_running(self):
        self.responder = Thread(target=self.worker, name='Response thread')
        self.responder.daemon = True
        self.responder.start()
        
    def integrate_sound_menu(self):
        #sound menu integration
        self.sound_menu = SoundMenuControls('xbmcremote')
        self.sound_menu._sound_menu_next = self.PlayNext
        self.sound_menu._sound_menu_previous = self.PlayPrevious
        self.sound_menu._sound_menu_pause = self.sound_menu._sound_menu_play = self.PlayPause
        self.sound_menu._sound_menu_is_playing = self.is_playing   
        self.sound_menu._sound_menu_raise = self.ui.show
        
    def connect_to_xbmc(self, from_refresh=False):
        try:
            self.send.getSocket(self.ip, self.port)
        except SocketError:
            self.connected = False
        else:
            self.connected = True
        finally:
            if not from_refresh:
                self.ui.refresh(False)
            
    def is_playing(self):
        return not self.paused

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
                identifier = item['id']
                callback = item['callback']
                #Show a nice error dialog or raise an exception
                if kind == 'error':
                    if identifier == 'state':
                        self.playing = False
                    else:
                        self.handle_error(data)
                #Use callbacks if the data is for something unconventional
                elif callback is not None:
                    callback(data)
                #Otherwise this will work out what to do with it
                elif data == 'OK':
                    print data
                elif kind == 'response':
                    if identifier == 'state' or identifier == 'control':
                        self.playing = data['playing']
                        self.paused = data['paused']
                        self.ui.paused(self.paused)
                        if data['paused']:
                            self.sound_menu.signal_paused()
                        else:
                            self.sound_menu.signal_playing()
                    elif self.ui.methods.has_key(identifier):
                        self.ui.methods[identifier](data)
                    else:
                        print data
                elif kind == 'announcement':
                    if data == 'PlaybackStarted':
                        self.playing = True
                    elif data == 'PlaybackStopped':
                        self.playing = False
                    elif data == 'PlaybackPaused':
                        self.paused = True
                    elif data == 'PlaybackResumed':
                        self.paused = False
                    else:
                        print data
                else:
                    print 'Weirdly,', data
            except Exception as ex:
                #TODO Do something
                print 'Error:', ex
    
    def handle_error(self, error):
        self.ui.handle_error(error)
        
    def kill(self):
        self.send.closeSocket()
        self.killed = True

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
        
