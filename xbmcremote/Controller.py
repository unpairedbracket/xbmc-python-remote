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


from xbmcremote_lib.JsonObjects import XJ
from xbmcremote_lib.XbmcRemoteObject import XbmcRemoteObject
from Queue import Queue
from threading import Thread
from socket import error as SocketError

class Controller(XbmcRemoteObject):

    def __init__(self, application):
        XbmcRemoteObject.__init__(self, application)
        self.control_methods = {
                'play': self.PlayPause,
                'next': self.PlayNext,
                'prev': self.PlayPrevious,
                'start': self.StartPlaying,
                'pause': self.PlayPause,
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

        self.XJ = XJ

        self.queue = Queue()

        self.connect('xbmc_get', self.get_data)
        self.connect('xbmc_control', self.send_control)
        self.connect('xbmc_init', self.start_running)

    def start_running(self, signaller, data=None):
        self.responder = Thread(target=self.worker, name='Response thread')
        self.responder.daemon = True
        self.responder.start()

    def get_data(self, interface, request, params):
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

    def add(self, data):
        self.queue.put(data)

    def worker(self):
        while True:
            try:
                item = self.queue.get()
                kind = item['kind']
                data = item['data']
                identifier = item['id']
                #Show a nice error dialog or print the error
                if kind == 'error':
                    self.handle_error(item)
                #This will work out what to do with responses and notifications
                elif data == 'OK':
                    #This tells us exactly nothing useful
                    pass
                elif kind == 'response':
                    if identifier == 'now_playing':
                        self.emit("xbmc_new_playing", data['item']['artist'], data['item']['album'], data['item']['title'])
                    elif data.has_key('speed'):
                        self.set_speed(data['speed'])
                    else:
                        self.emit('xbmc_response', identifier, data)
                elif kind == 'notification':
                    if identifier == 'Player.OnPlay' and not self.state['paused']:
                        #This can mean unpaused or new song.
                        #Check now playing just in case.
                        self.GetNowPlaying()
                    if identifier in ['Player.OnPlay', 'Player.OnPause']:
                        self.state['player'] = data['player']['playerid']
                        self.set_speed(data['player']['speed'])
                        self.state['playing'] = True
                    else:
                        print data
                else:
                    print 'Weirdly,', data
            except Exception as ex:
                #TODO Do something
                print 'Processing error:', ex

    def set_speed(self, speed):
        if speed == 0:
            self.state['paused'] = True
        elif speed == 1:
            self.state['paused'] = False
        self.state['playing'] = True
        self.emit('xbmc_paused', self.state['paused'])
        #TODO signal this

    def handle_error(self, error):
        message = error['data']['message']
        code =  error['data']['code']
        identifier = error['id']
        self.emit("xbmc_error", message, code, identifier)

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
        artistid = int(data[0])
        action = self.XJ.GetAlbums(artistid)
        self.json_send(action, timeout=0.5)

    def GetSongs(self, data=[-1,-1]):
        artistid = int(data[0])
        albumid = int(data[1])
        action = self.XJ.GetSongs(artistid, albumid)
        self.json_send(action, timeout=0.5)

    def GetNowPlaying(self, data=[]):
        action = self.XJ.GetNowPlaying(self.state['player'])
        self.json_send(action)

    def GetPlayers(self, data=[]):
        action = self.XJ.GetPlayers()
        self.json_send(action)

    def SendCustomRequest(self, data=[-1,-1,-1,-1]):
        print data
        method = str(data[0])
        params = str(data[1])
        timeout = float(data[2])
        action = self.XJ.JsonRpc.Custom.__getattr__(method)(params, identifier='custom')
        self.json_send(action, timeout)

    def json_send(self, json, timeout=0.1):
        """General method for emitting the xbmc_send signal"""
        self.emit("xbmc_send", json, timeout)
