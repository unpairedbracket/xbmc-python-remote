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

import json

class JsonBuilder(object):
    """Smartly builds json requests"""
    def __init__(self, name=None):
        #If name specified, use name.method
        try:
            self.name = name + '.'
        #Otherwise just use method
        except Exception, e:
            self.name = ''

        self.encoder = json.JSONEncoder()

    def __getattr__(self, attr):
        method = self.name + attr
        return self.make_method(method)

    def make_method(self, method_name):
        def method(identifier = 1, **params):
            json = self.build_json(method_name, params, identifier)
            return json
        return method

    def build_json(self, method, params, identifier):
        jsonstring = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': identifier}
        return self.encoder.encode(jsonstring)
