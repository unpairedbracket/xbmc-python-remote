# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Ben Spiers
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
Parent class for most of the program's objects. Provides GObject signal
connection and emission methods and access to the server player state and
program settings.
'''

import logging

class XbmcRemoteObject(object): # pylint: disable=R0903
    '''
    Subclass this for objects that need access to the server state, 
    application settings, and signal emission and reception.
    '''

    def __init__(self, application):
        self.application = application
        self.settings = application.settings
        self.state = application.state
        self.signals = self.application.signals
        self.signal_connect = self.signals.connect
        self.emit = self.signals.emit
        self.logger = logging.getLogger('xbmcremote')
