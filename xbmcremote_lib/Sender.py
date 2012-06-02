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
from Queue import Queue
from threading import Thread
from gi.repository import GObject

class Sender(GObject.GObject):

    def __init__(self, controller):
        GObject.GObject.__init__(self)
        controller.connect("xbmc_send", self.add)
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.queue = Queue()
        self.controller = controller
        self.start()
        
    def getSocket(self, IpAddress, Port):
        self.__s.connect((IpAddress, Port))
        
    def closeSocket(self):
        self.__s.shutdown(socket.SHUT_RDWR)
        self.__s.close()

    def add(self, controller, json, callback, timeout, data=None):
        data = {'json': json, 'callback': callback, 'timeout': timeout}
        self.queue.put(data)
            
    def start(self):
        self.work = Thread(target=self.worker, name='Network thread')
        self.work.daemon = True
        self.work.start()

    def worker(self):
        while True:
            try:
                item = self.queue.get()
                json = item['json']
                callback = item['callback']
                timeout = item['timeout']
                self.__send(json, callback, timeout)
            except Exception as ex:
                #TODO Do something
                print ex
    
    def __send(self, json, callback, timeout):
        self.__s.send(json)
        #Some functions take unusually long to respond to
        self.__s.settimeout(timeout)
        responses = ''
        while True:
            try: 
                responses += self.__returnResponse()
            except socket.timeout:
                return self.controller.sendCallback(responses, callback)

    def __returnResponse(self):    
        response = ''
        while True:
            response += (self.__s.recv(0x4000))
    
            if len(select.select([self.__s], [], [], 0)[0]) == 0:
                return response;