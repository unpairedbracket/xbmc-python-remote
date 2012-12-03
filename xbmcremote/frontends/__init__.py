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
This module contains the BaseFrontend class.
It should be the parent of all Frontends
and should never be instantiated itself
'''

from xbmcremote_lib.XbmcRemoteObject import XbmcRemoteObject
from threading import Thread
from ast import literal_eval


class BaseFrontend(XbmcRemoteObject):

    '''This is the main parent that all frontends should inherit from'''

    def __init__(self, application):
        XbmcRemoteObject.__init__(self, application)
        self.loop = None
        self.methods = {}
        self.signal_connect('xbmc_error', self.handle_error)
        self.signal_connect('xbmc_frontend_init', self.thread_loop)
        self.signal_connect('xbmc_response', self.use_response)
        self.signal_connect('xbmc_paused', self.paused)

    def use_response(self, signaller, method, response, data=None):
        '''
        Called when a response is processed so that subclasses
        can use it.
        '''
        if method in self.methods:
            self.methods[method](literal_eval(response))

    def refresh(self, signaller, data=True):
        '''
        Override this to refresh the frontend before starting its main loop.
        '''
        pass

    def handle_error(self, signaller, error, data=None):
        '''
        Override this to cope with errors in special ways,
        such as showing a dialog.
        '''
        pass

    def show(self):
        '''
        Override this to show a window if there is one,
        using Gtk.Window.show(), or bring the terminal window
        to the foreground if there is one of those.
        '''
        pass

    def thread_loop(self, signaller, data=None):
        '''
        This allows main control of the program to be transferred
        to a new thread via the xbmc_frontend_init signal.
        '''
        name = self.__class__.__name__
        self.loop = Thread(target=self.start_loop, name=name + ' thread')
        self.loop.start()

    def start_loop(self):
        '''
        Override this and start the main loop of the Frontend,
        using Gtk.main() for gtk windows or some kind of
        interactive interpreter for a terminal frontends.
        '''
        pass

    def paused(self, signaller, paused, data=None):
        '''
        Called when a response is received that
        indicates the server is (un)paused
        '''
        pass
