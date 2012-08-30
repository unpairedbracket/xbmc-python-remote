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

'''Module contains Controller class'''

from xbmcremote_lib.JsonObjects import xbmc_json
from xbmcremote_lib.XbmcRemoteObject import XbmcRemoteObject
from Queue import Queue
from threading import Thread
from ast import literal_eval


class Controller(XbmcRemoteObject):

    '''
    Controller -- Class in charge of sending json strings to the network 
    thread to be sent and dealing with responses to them
    '''

    def __init__(self, application):
        XbmcRemoteObject.__init__(self, application)
        self.xbmc_json = xbmc_json
        self.responder = Thread(target=self.worker, name='Response thread')
        self.responder.daemon = True
        self.songid = -1
        self.control_methods = {
            'play': self.play_pause,
            'next': self.play_next,
            'prev': self.play_previous,
            'start': self.start_playing,
            'pause': self.play_pause,
            'stop': self.stop_playing,
            'artists': self.get_artists,
            'albums': self.get_albums,
            'songs': self.get_songs,
            'state': self.check_state,
            'now_playing': self.get_now_playing,
            'current_position': self.get_position,
            'play_now': self.play_song_now,
            'play_next': self.play_song_next,
            'play_last': self.play_song_last,
            'custom': self.send_custom_request
        }

        self.queue = Queue()

        self.signal_connect('xbmc_control', self._send_control)
        self.signal_connect('xbmc_init', self._start_running)
        self.signal_connect('xbmc_decoded', self._add)

    def _start_running(self, signaller, data=None):
        '''Start the response thread running on xbmc_init signal'''
        if not self.responder.is_alive():
            self.responder.start()

    def _send_control(self, signaller, request, params, data=None):
        '''Call the appropriate method for a control signal'''
        try:
            paramdict = literal_eval(params)
        except ValueError:
            paramdict = {}
        try:
            self.control_methods[request](**paramdict)
        except KeyError:
            print 'No control method found for ', request

    def _add(self, signaller, message_string, data=None):
        '''Put a response into the queue for response thread to deal with'''
        message = literal_eval(message_string)
        self.queue.put(message)

    def worker(self):
        '''Process messages from xbmc and call the relevant handler method'''
        while True:
            try:
                message = self.queue.get()
                kind = message['kind']
                data = message['data']
                identifier = message['id']
                print message
                if data == 'OK':
                    #This tells us exactly nothing
                    pass
                elif kind == 'error':
                    self.handle_error(message)
                elif kind == 'response':
                    self._handle_response(data, identifier)
                elif kind == 'notification':
                    self._handle_notification(data, identifier)
                else:
                    print 'Weirdly,', data
            except Exception as ex:
                print 'Processing error:', ex

    def _handle_response(self, data, identifier):
        '''Handle a response from xbmc'''
        if identifier == 'get_position_for_play_now':
            next_position = data['position'] +1
            self.insert_and_play(self.songid, next_position)
        if identifier == 'get_position_for_play_next':
            next_position = data['position'] + 1
            self.insert_song(self.songid, next_position)
        if 'speed' in data:
            self.set_speed(data['speed'])
        self.emit('xbmc_response', identifier, data)

    def _handle_notification(self, data, identifier):
        '''Handle a notification from xbmc'''
        if identifier == 'Player.OnPlay' and not self.state['paused']:
            self.get_now_playing()
        elif identifier == 'Player.OnStop':
            self.state['playing'] = False
        if identifier in ['Player.OnPlay', 'Player.OnPause']:
            self.state['player'] = data['player']['playerid']
            self.set_speed(data['player']['speed'])
            self.state['playing'] = True
        else:
            print data

    def set_speed(self, speed):
        '''Set the state when the server informs us of the speed'''
        if speed == 0:
            self.state['paused'] = True
        elif speed == 1:
            self.state['paused'] = False
        self.state['playing'] = True
        self.emit('xbmc_paused', self.state['paused'])

    def handle_error(self, error):
        '''Handle any error messages the server sends back'''
        self.emit("xbmc_error", error)

    def play_pause(self):
        '''Send the play/pause signal'''
        action = self.xbmc_json.play()
        print action
        self._json_send(action)

    def play_next(self):
        '''Send the play next signal'''
        action = self.xbmc_json.next()
        self._json_send(action)

    def play_previous(self):
        '''Send the play previous signal'''
        action = self.xbmc_json.prev()
        self._json_send(action)

    def start_playing(self, songid=None):
        '''Send the start playing signal'''
        action = self.xbmc_json.start()
        if songid is not None:
            queue = self.xbmc_json.queue_song(songid)
            action = ''.join(['[', queue, ',', action, ']'])
        self._json_send(action)

    def stop_playing(self):
        '''Send the stop playing signal'''
        action = self.xbmc_json.stop()
        self._json_send(action)

    def check_state(self):
        '''Send the check state signal'''
        action = self.xbmc_json.state()
        self._json_send(action)

    def get_artists(self):
        '''Send a request for the list of artists'''
        action = self.xbmc_json.get_artists()
        self._json_send(action, timeout=0.5)

    def get_albums(self, artistid=-1):
        '''Send a request for the list of albums'''
        action = self.xbmc_json.get_albums(artistid)
        self._json_send(action, timeout=0.5)

    def get_songs(self, artistid=-1, albumid=-1):
        '''Send a request for the list of songs'''
        action = self.xbmc_json.get_songs(artistid, albumid)
        self._json_send(action, timeout=0.5)

    def get_now_playing(self):
        '''Send a request for the currently playing item'''
        action = self.xbmc_json.get_now_playing(self.state['player'])
        self._json_send(action)

    def get_position(self, identifier='current_position'):
        '''Find out where we are in the playlist'''
        action = self.xbmc_json.get_position(identifier)
        self._json_send(action)

    def play_song_now(self, songid):
        '''Start the process of playing a song from the library immediately'''
        self.songid = songid
        if self.state['playing']:
            self.get_position('get_position_for_play_now')
        else:
            self.start_playing(songid=songid)

    def play_song_next(self, songid):
        '''Start the process of playing a song from the library next'''
        self.songid = songid
        if self.state['playing']:
            self.get_position('get_position_for_play_next')
        else:
            self.start_playing(songid)

    def play_song_last(self, songid):
        '''Start the process of playing a song from the library next'''
        self.songid = songid
        if self.state['playing']:
            action = self.xbmc_json.queue_song(songid)
            self._json_send(action)
        else:
            self.start_playing(songid)

    def insert_song(self, songid, position):
        '''Insert the song'''
        action = self.xbmc_json.insert_song(songid, position)
        self._json_send(action)

    def insert_and_play(self, songid, position):
        '''Insert and play the song'''
        action = self.xbmc_json.insert_and_play(songid, position)
        self._json_send(action)

    def send_custom_request(self, method, params,
                            identifier='custom', timeout=0.5):
        '''Send a custom method and parameters'''
        action = self.xbmc_json.custom_method(method, params, identifier)
        self._json_send(action, timeout)

    def _json_send(self, json, timeout=0.1):
        '''General method for emitting the xbmc_send signal'''
        self.emit("xbmc_send", json, timeout)
