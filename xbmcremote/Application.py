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


from xbmcremote_lib.Sender import Sender
from xbmcremote_lib.Decoder import Decoder
from xbmcremote_lib.Signals import Signals
from xbmcremote.Controller import Controller
from gi.repository import Gio

class Application(object):

    def __init__(self, gui):

        self.settings = Gio.Settings("net.launchpad.xbmcremote")
        self.state = {
                        'playing': False, 'paused': False,
                        'player': 0, 'ip': '', 'port': 0,
                        'connected':False
                     }

        self.signals = Signals()
        self.emit = self.signals.emit

        self.controller = Controller(self)
        self.send = Sender(self)
        self.decoder = Decoder(self)

        self.interfaces = []
        if gui:
            from interfaces.GtkInterface import GtkInterface
            self.interfaces.append(GtkInterface)
        else:
            from interfaces.TextInterface import TextInterface
            self.interfaces.append(TextInterface)
        if self.settings.get_boolean('mpris2'):
            from interfaces.SoundMenuInterface import SoundMenuInterface
            self.interfaces.append(SoundMenuInterface)

        self.interface_instances = []
        for Interface in self.interfaces:
            self.interface_instances.append(Interface(self))

        self.emit('xbmc_init')
        self.emit('xbmc_interface_init')

    def kill(self):
        self.send.closeSocket()
        self.killed = True

