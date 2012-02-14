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

from json import JSONDecoder

class Decoder(object):
    
    def __init__(self, controller):
        self.decoder = JSONDecoder()
        self.controller = controller
    
    def decode(self, Json, callback=None):
        js = self.decoder.decode(Json)
        for i in js:
            #check for a valid response
            if i.has_key('error'):
                kind = 'error'
                identifier = i['id']
                result = i['error']
            elif i.has_key('result'):
                kind = 'response'
                identifier = i['id']
                result = i['result']
            elif (i.has_key('method')) and (i['method'] == 'Announcement'):
                kind = 'announcement'
                identifier = None
                result = i['params']['message']
                
            data = {'kind': kind, 'data': result, 'callback': callback, 'id': identifier}
            self.controller.add(data)
