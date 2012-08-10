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

from xbmcremote.interfaces import BaseInterface
import time
import readline

class TextInterface(BaseInterface):

    def __init__(self, application):
        self.loop = None
        BaseInterface.__init__(self, application)
        self.controls = ['next', 'prev', 'play', 'pause', 'start', 'stop']
        self.requests = ['artists', 'albums', 'songs', 'state', 'players',
                         'now_playing']

    def start_loop(self):
        while True:
            time.sleep(0.5)
            command = raw_input('What should I do? ')
            if command in self.controls:
                self.emit('xbmc_control', command, None)
            elif command in self.requests:
                self.emit('xbmc_get', command, None)
            elif command == 'exit':
                break
            elif '.' in command:
                self.emit('xbmc_get', 'custom', command + ' {} 0.5')
            else:
                print 'Unknown command'

    def echo(self, message):
        print message

    def paused(self, signaller, paused, data=None):
        if paused:
            print 'Playback Paused'
        else:
            print 'Playback Unpaused'
