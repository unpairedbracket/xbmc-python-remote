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

import socket
import select
from Queue import Queue, Empty
from threading import Thread
from gi.repository import GObject

class Sender(GObject.GObject):

    __gsignals__ = {
            "xbmc_received": (GObject.SIGNAL_RUN_FIRST, None, (str,))
        }

    def __init__(self, controller):
        GObject.GObject.__init__(self)
        controller.connect("xbmc_send", self.add)
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.queue = Queue()
        self.recv_queue = Queue()
        self.controller = controller
        self.start()
        
    def getSocket(self, IpAddress, Port):
        self.__s.connect((IpAddress, Port))
        
    def closeSocket(self):
        self.__s.shutdown(socket.SHUT_RDWR)
        self.__s.close()

    def add(self, signaller, json, timeout, data=None):
        data = {'json': json, 'timeout': timeout}
        self.queue.put(data)
            
    def start(self):
        self.work = Thread(target=self.worker, name='Network sender thread')
        self.work.daemon = True
        self.work.start()
        self.recv = Thread(target=self.recver, name='Network receiver thread')
        self.recv.daemon = True
        self.recv.start()

    def worker(self):
        """sends messages to xbmc"""
        while True:
            try:
                item = self.queue.get()
                json = item['json']
                timeout = item['timeout']
                self.__s.send(json)
                self.recv_queue.put(timeout)
            except Exception as ex:
                #TODO Do something
                print 'Sender error: ', ex

    def recver(self):
        """receives messages from xbmc"""
        while True:
            try:
                try:
                    timeout = self.queue.get(True, 2.0)
                except Empty:
                    timeout = 1.0
                try:
                    responses = ''
                    response = ''
                    self.__s.settimeout(timeout)
                    while True:
                        response += (self.__s.recv(0x4000))
                        if len(select.select([self.__s], [], [], 0)[0]) == 0:
                            responses += response
                            response = ''
                except socket.timeout:
                #A timeout means there really is nothing left
                #so the response is complete
                    #Just need to 'normalise' the responses
                    #in case there's more than one in there
                    responses = '[' + responses.replace('}\n{', '},{').replace('}{','},{') + ']'
                    self.emit("xbmc_received", responses)
            except Exception as ex:
                print 'Reveiver error: ', ex

