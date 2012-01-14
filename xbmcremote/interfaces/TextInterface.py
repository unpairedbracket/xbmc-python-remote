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

from xbmcremote_lib.DummyInterface import BaseInterface
import time

class TextInterface(BaseInterface):
    
    def __init__(self, controller):
        super(TextInterface, self).__init__(controller)
        self.commands = {'next': self.controller.PlayNext, 'prev': self.controller.PlayPrevious, 'play': self.controller.PlayPause,
                         'pause': self.controller.PlayPause, 'start': self.controller.StartPlaying, 'stop': self.controller.StopPlaying}
        
    def start_loop(self):        
        while True:
            time.sleep(0.5)
            command = raw_input("What should I do? ")
            if command in self.commands:
                self.commands[command]()
            elif command == 'exit':
                break
            elif '.' in command:
                self.controller.SendCustomRequest(command, callback=self.echo)
            else:
                print 'Unknown command'
                
    def handle_error(self, error):
        print 'Error:', error['message'], 'Code:', error['code']
    
    def echo(self, message):
        print message

                
    def paused(self, paused):
        if paused:
            print 'Playback Paused'
        else:
            print 'Playback Unpaused'