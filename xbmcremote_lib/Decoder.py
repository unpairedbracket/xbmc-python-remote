# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Ben Spiers 
# 
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

'''
Decodes the messages sent by XBMC and extracts the useful information from them
'''

from json import JSONDecoder
from xbmcremote_lib.XbmcRemoteObject import XbmcRemoteObject

class Decoder(XbmcRemoteObject):
    '''
    Class that picks up messages received by Sender and decodes them, then
    passes them on to Controller
    '''

    def __init__(self, application):
        XbmcRemoteObject.__init__(self, application)
        self.decoder = JSONDecoder()
        self.signal_connect("xbmc_received", self.add)

    def add(self, signaller, json, data=None):
        '''Generate a python object from the json string'''
        json_object = self.decoder.decode(json)
        self.decode(json_object)

    def decode(self, json_object):
        '''
        Extract the important information from a list of dictionaries or lists
        '''

        for response in json_object:
            if isinstance(response, list):
                # The response could actually be a list of responses
                print 'recursing'
                self.decode(response)
            else:
                # Otherwises the response will be a dictionary.
                if 'error' in response:
                    print 'decoded error'
                    kind = 'error'
                    identifier = response['id']
                    result = response['error']
                elif 'result' in response:
                    print 'decoded result'
                    kind = 'response'
                    identifier = response['id']
                    result = response['result']
                elif 'method' in response:
                    print 'decoded notification'
                    if response['method'] == 'Announcement':
                        kind = 'announcement'
                        identifier = None
                        result = response['params']['message']
                    else:
                        kind = 'notification'
                        identifier = response['method']
                        result = response['params']['data']
                else:
                    break

                data = {'kind': kind, 'data': result, 'id': identifier}
                self.emit('xbmc_decoded', data)
