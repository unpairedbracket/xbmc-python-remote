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

'''
This module is the base of the JSON-RPC implementation. I wrote it for XBMC's
JSON-RPC API but it should actually work for any JSON-RPC.
'''

from json import JSONEncoder

class JsonBuilder(object):
    '''Smartly builds json requests'''
    def __init__(self, namespace=None):
        #If name specified, use namespace.method
        try:
            self.namespace = namespace + '.'
        #Otherwise just use method
        except TypeError:
            self.namespace = ''

        self.encoder = JSONEncoder()

    def __getattr__(self, attr):
        '''
        This makes undefined identifiers into methods, so that API methods
        can be called like real ones
        '''
        method_name = ''.join([self.namespace, attr])
        return self.make_method(method_name)

    def make_method(self, method_name):
        ''''Creates a method to build JSON requests for method names'''
        def method(identifier = 'xbmcremote', **params):
            '''
            This method will act as a replacement for any undefined
            identifierthat is called
            '''
            json = self.build_json(method_name, params, identifier)
            return json
        return method

    def build_json(self, method, params, identifier):
        '''Builds the JSON request for the method, params and identifier'''
        if params is None:
            params = {}
        jsonstring = {'jsonrpc': '2.0', 'method': method, 'params': params, 
                      'id': identifier}
        return self.encoder.encode(jsonstring)
