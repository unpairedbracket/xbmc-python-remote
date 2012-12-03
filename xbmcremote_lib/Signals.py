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
Contains Signals, a GObject that contains all of Xbmcremote's GSignals
'''

from gi.repository import GObject
import logging

class Signals(GObject.GObject): # pylint: disable=W0232

    '''
    Signals contains all of the signals used in the program. It is 
    instantiated once as a singleton and its connect and emit methods are used
    by XbmcRemoteObject subclasses to pass information around the program.
    '''

    __gsignals__ = {
            "xbmc_init": (GObject.SIGNAL_RUN_FIRST, None, ()),
            "xbmc_frontend_init": (GObject.SIGNAL_RUN_FIRST, None, ()),
            "xbmc_reconnect": (GObject.SIGNAL_RUN_FIRST, None, ()),
            "xbmc_connected": (GObject.SIGNAL_RUN_FIRST, None, ()),
            "xbmc_disconnected": (GObject.SIGNAL_RUN_FIRST, None, ()),
            "xbmc_control": (GObject.SIGNAL_RUN_FIRST, None, (str, str,)),
            "xbmc_send": (GObject.SIGNAL_RUN_FIRST, None, (str, float)),
            "xbmc_received": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
            "xbmc_decoded": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
            "xbmc_response": (GObject.SIGNAL_RUN_FIRST, None, (str, str,)),
            "xbmc_paused": (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
            "xbmc_error": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
            "xbmc_kill": (GObject.SIGNAL_RUN_FIRST, None, ()),
        }

    logger = logging.getLogger('xbmcremote_lib')

    def do_xbmc_init(self, *data):
        '''debug logging for xbmc_init signal'''
        self.logger.debug("Signal: init "+str(data))

    def do_xbmc_frontend_init(self, *data):
        '''debug logging for xbmc_frontend_init signal'''
        self.logger.debug("Signal: frontend_init "+str(data))

    def do_xbmc_reconnect(self, *data):
        '''debug logging for xbmc_reconnect signal'''
        self.logger.debug("Signal: reconnect "+str(data))

    def do_xbmc_connected(self, *data):
        '''debug logging for xbmc_connected signal'''
        self.logger.debug("Signal: connected "+str(data))

    def do_xbmc_disconnected(self, *data):
        '''debug logging for xbmc_disconnected signal'''
        self.logger.debug("Signal: disconnected "+str(data))

    def do_xbmc_control(self, *data):
        '''debug logging for xbmc_control signal'''
        self.logger.debug("Signal: control "+str(data))

    def do_xbmc_send(self, *data):
        '''debug logging for xbmc_send signal'''
        self.logger.debug("Signal: send "+str(data))

    def do_xbmc_received(self, *data):
        '''debug logging for xbmc_received signal'''
        self.logger.debug("Signal: received "+str(data))

    def do_xbmc_decoded(self, *data):
        '''debug logging for xbmc_decoded signal'''
        self.logger.debug("Signal: decoded "+str(data))

    def do_xbmc_response(self, *data):
        '''debug logging for xbmc_response signal'''
        self.logger.debug("Signal: response "+str(data))

    def do_xbmc_paused(self, *data):
        '''debug logging for xbmc_paused signal'''
        self.logger.debug("Signal: paused "+str(data))

    def do_xbmc_error(self, *data):
        '''debug logging for xbmc_error signal'''
        self.logger.debug("Signal: error "+str(data))

    def do_xbmc_kill(self, *data):
        '''debug logging for xbmc_kill signal'''
        self.logger.debug("Signal: kill "+str(data))
