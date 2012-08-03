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


from xbmcremote_lib.Sender import Sender
from xbmcremote_lib.Decoder import Decoder
from xbmcremote_lib.sound_menu import SoundMenuControls
from xbmcremote_lib.JsonObjects import XJ
from gi.repository import GObject, Gio
from Queue import Queue
from threading import Thread
from socket import error as SocketError

class Controller(GObject.GObject):
    __gsignals__ = {
            "xbmc_init": (GObject.SIGNAL_RUN_FIRST, None, ()),
            "xbmc_send": (GObject.SIGNAL_RUN_FIRST, None, (str, float)),
        }


    def __init__(self, gui):
        GObject.GObject.__init__(self)
        self.gui = gui
        if self.gui:
            from interfaces.GtkInterface import GtkInterface as Interface
        else:
            from interfaces.TextInterface import TextInterface as Interface

        self.control_methods = {
                'play': self.PlayPause,
                'next': self.PlayNext,
                'prev': self.PlayPrevious,
                'start': self.StartPlaying,
                'stop': self.StopPlaying
            }

        self.data_methods = {
                'artists': self.GetArtists,
                'albums': self.GetAlbums,
                'songs': self.GetSongs,
                'state': self.CheckState,
                'players': self.GetPlayers,
                'now_playing':self.GetNowPlaying,
                'custom': self.SendCustomRequest
            }
        self.settings = Gio.Settings("net.launchpad.xbmcremote")
        
        self.XJ = XJ
        self.ui = Interface(self)

        self.sound_menu_integration = self.settings['mpris2']
        self.connected = False
        self.queue = Queue()
        
        #Initialise parts
        self.send = Sender(self)
        self.decoder = Decoder(self)
        
        #Start program running with responder thread
        self.start_running()
        
        self.playing = self.paused = False

        #Server settings
        self.ip = self.settings.get_string('ip-address')
        self.port = int(self.settings.get_string('port'))
        
        if self.sound_menu_integration:
            self.integrate_sound_menu()
        
        self.ui.show()
        self.ui.refresh()
        self.ui.start_loop()
        
    def start_running(self):
        self.responder = Thread(target=self.worker, name='Response thread')
        self.responder.daemon = True
        self.responder.start()
        
    def get_data(self, interface, request, params):
        print params
        try:
            paramlist = params.split()
        except:
            self.data_methods[request]()
        else:
            self.data_methods[request](paramlist)

    def send_control(self, interface, request, params):
        try:
            paramlist = params.split()
        except:
            self.control_methods[request]()
        else:
            self.control_methods[request](paramlist)

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
            self.initialise_connection()
        finally:
        #TODO This is bad, mmkay
            if not from_refresh:
                self.ui.refresh(False)

    def initialise_connection(self):
        self.emit('xbmc_init')

    def do_xbmc_init(instance):
        print 'init'

    def is_playing(self):
        return not self.paused

    def add(self, data):
        self.queue.put(data)

    def sendCallback(self, jsonlist, callback):
        json = '[' + jsonlist.replace('}\n{', '},{').replace('}{','},{') + ']'
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
                    self.handle_error(data)
                #Use callbacks if the data is for something unconventional
                elif callback is not None:
                    callback(data)
                #Otherwise this will work out what to do with it
                elif data == 'OK':
                    print data
                elif kind == 'response':
                    if identifier == 'state' or identifier == 'control':
                        if data.has_key('playing'):
                            if data['paused']:
                                self.set_speed(0)
                            else:
                                self.set_speed(1)
                            self.paused = data['paused']
                            self.ui.paused(self.paused)
                            if self.sound_menu_integration:
                                if data['paused']:
                                    self.sound_menu.signal_paused()
                                else:
                                    self.sound_menu.signal_playing()
                        if data.has_key('speed'):
                            self.set_speed(data['speed'])
                    elif data.has_key('speed'):
                            self.set_speed(data['speed'])
                    elif self.ui.methods.has_key(identifier):
                        self.ui.methods[identifier](data)
                    else:
                        print data
                elif kind == 'notification':
                    if data.has_key('player'):
                        self.set_speed(data['player']['speed'])
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
                
    def set_speed(self, speed):
        if speed == 0:
            self.paused = True
        elif speed == 1:
            self.paused = False
        self.playing = True
        self.ui.paused(self.paused)
        if self.sound_menu_integration:
            self.sound_menu.send_signal(self.paused)
    
    def handle_error(self, error):
        self.ui.handle_error(error)
        
    def kill(self):
        self.send.closeSocket()
        self.killed = True

    def PlayPause(self, data=[]):
        action = self.XJ.XBMC_PLAY
        self.json_send(action)

    def PlayNext(self, data=[]):
        action = self.XJ.XBMC_NEXT
        self.json_send(action)

    def PlayPrevious(self, data=[]):
        action = self.XJ.XBMC_PREV
        self.json_send(action)

    def StartPlaying(self, data=[]):
        action = self.XJ.XBMC_START
        self.json_send(action)

    def StopPlaying(self, data=[]):
        action = self.XJ.XBMC_STOP
        self.json_send(action)

    def CheckState(self, data=[]):
        action = self.XJ.XBMC_STATE
        self.json_send(action)

    def GetArtists(self, data=[]):
        action = self.XJ.GetArtists()
        self.json_send(action, timeout=0.5)

    def GetAlbums(self, data=[-1]):
        print data
        artistid = int(data[0])
        action = self.XJ.GetAlbums(artistid)
        self.json_send(action, timeout=0.5)

    def GetSongs(self, data=[-1,-1]):
        artistid = int(data[0])
        albumid = int(data[1])
        action = self.XJ.GetSongs(artistid, albumid)
        self.json_send(action, timeout=0.5)

    def GetNowPlaying(self, data=[]):
        action = self.XJ.GetNowPlaying(0) #TODO: Use a player number from XBMC
        self.json_send(action)

    def GetPlayers(self, data=[]):
        action = self.XJ.GetPlayers()
        self.json_send(action)

    def SendCustomRequest(self, data=[-1,-1,-1,-1]):
        method = int(data[0])
        params = int(data[1])
        callback = eval(data[2])
        timeout = float(data[3])
        action = self.XJ.XbmcJson.Custom.__getattr__(method)(params, identifier='custom')
        self.json_send(action, callback, timeout)

    def json_send(self, json, callback=None, timeout=0.1):
        """General method for emitting the xbmc_send signal"""
        self.emit("xbmc_send", json, callback, timeout)
