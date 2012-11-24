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
Module contains TextFrontend class.
'''

import time
import readline
from ast import literal_eval

from xbmcremote.frontends import BaseFrontend


class TextFrontend(BaseFrontend):
    '''
    Terminal-based command line frontend.

    This can be particularly useful for debugging as it contains methods for
    sending arbitrary API calls to xbmc
    '''

    def __init__(self, application):
        self.loop = None
        BaseFrontend.__init__(self, application)
        self.controls = ['next', 'prev', 'play', 'pause', 'start', 'stop',
                         'artists', 'albums', 'songs', 'state', 'players',
                         'now_playing', 'current_position']
        self.methods = {'custom': self.echo}

    def start_loop(self):
        while True:
            time.sleep(0.5)
            command = raw_input('What should I do? ')
            if command in self.controls:
                self.emit('xbmc_control', command, None)
            elif command.startswith('play_song'):
                commandlist = command.split(' ')
                print commandlist
                self.emit('xbmc_control', commandlist[0], 
                          {'songid': int(commandlist[1])})
            elif '.' in command:
                self.send_custom(command)
            elif command == 'exit':
                break
            else:
                print 'Unknown command'

    def send_custom(self, command):
        '''
        Construct a custom command to send to xbmc.
        
        The command typed in should be in the form 
            Namespace.Method('param1': 1, 'param2': 2, 'param3': 3)
        to call the method Namespace.Method with params
            {'param1': 1, 'param2': 2, 'param3': 3}
        '''
        customcommand = {}
        if command[-1] == ')':
            command_list = command[:-1].split('(')
        else:
            command_list = [command, '']

        customcommand['method'] = command_list[0]
        paramstring = ''.join(['{', command_list[1], '}'])
        customcommand['params'] = literal_eval(paramstring)

        self.emit('xbmc_control', 'custom', customcommand)

    def handle_error(self, signaller, error, data=None):

        error = literal_eval(error)
        message = error['data']['message']
        code = error['data']['code']
        print 'Server error ' + str(code) + ': ' + message

    @staticmethod
    def echo(message):
        """Signal handler function wrapper for print statement"""
        print message

    def paused(self, signaller, paused, data=None):
        if paused:
            print 'Playback Paused'
        else:
            print 'Playback Unpaused'
