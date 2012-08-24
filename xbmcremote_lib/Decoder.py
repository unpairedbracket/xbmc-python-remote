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

from json import JSONDecoder
from xbmcremote_lib.XbmcRemoteObject import XbmcRemoteObject

class Decoder(XbmcRemoteObject):

    def __init__(self, application):
        XbmcRemoteObject.__init__(self, application)
        self.decoder = JSONDecoder()
        self.signal_connect("xbmc_received", self.add)

    def add(self, signaller, json, data=None):
        js = self.decoder.decode(json)
        self.decode(js)

    def decode(self, obj):
        for i in obj:
            if isinstance(i, list):
                self.decode(i)
            else:
                #check for a valid response
                if 'error' in i:
                    kind = 'error'
                    identifier = i['id']
                    result = i['error']
                elif 'result' in i:
                    kind = 'response'
                    identifier = i['id']
                    result = i['result']
                elif 'method' in i:
                    if i['method'] == 'Announcement':
                        kind = 'announcement'
                        identifier = None
                        result = i['params']['message']
                    else:
                        kind = 'notification'
                        identifier = i['method']
                        result = i['params']['data']
                else:
                    break

                data = {'kind': kind, 'data': result, 'id': identifier}
                self.emit('xbmc_decoded', data)
