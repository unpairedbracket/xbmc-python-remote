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

import socket
import select
from Queue import Queue, Empty
from threading import Thread
from xbmcremote_lib.XbmcRemoteObject import XbmcRemoteObject

class Sender(XbmcRemoteObject):

    def __init__(self, controller):
        XbmcRemoteObject.__init__(self, controller)
        self.signal_connect("xbmc_init", self.socket_connect)
        self.signal_connect("xbmc_reconnect", self.socket_connect)
        self.signal_connect("xbmc_connected", self.start)
        self.signal_connect("xbmc_send", self.add)
        self.signal_connect("xbmc_kill", self.close_socket)
        self.work = Thread(target=self.worker, name='Network sender thread')
        self.work.daemon = True
        self.queue = Queue()
        self.recv = Thread(target=self.recver, name='Network receiver thread')
        self.recv.daemon = True
        self.recv_queue = Queue()

    def socket_connect(self, signaller, data=None):
        ip = self.state['ip'] = self.settings.get_string('ip-address')
        port = self.state['port'] = int(self.settings.get_string('port'))
        connected = self.state['connected']
        if (not connected) or ((ip, port) != self.__socket.getpeername()):
        # Either the address has changed or we aren't connected
            try:
                # Create a new socket and connect
                self.__socket = socket.socket(socket.AF_INET,
                                              socket.SOCK_STREAM)
                self.__socket.settimeout(1)
                self.__socket.connect((ip, port))
            except socket.error:
                self.state['connected'] = False
                self.emit('xbmc_disconnected')
            else:
                self.state['connected'] = True
                self.emit('xbmc_connected')
        else:
            self.emit('xbmc_connected')

    def close_socket(self, signaller, data=None):
        self.__socket.shutdown(socket.SHUT_RDWR)
        self.__socket.close()

    def add(self, signaller, json, timeout, data=None):
        data = {'json': json, 'timeout': timeout}
        self.queue.put(data)

    def start(self, signaller, data=None):
        if not self.work.is_alive():
            self.work.start()
        if not self.recv.is_alive():
            self.recv.start()

    def worker(self):
        """sends messages to xbmc"""
        while True:
            try:
                item = self.queue.get()
                json = item['json']
                timeout = item['timeout']
                self.__socket.send(json)
                self.recv_queue.put(timeout)
            except Exception as ex:
                #TODO Do something
                print 'Sender error: ', ex

    def recver(self):
        """receives messages from xbmc"""
        while True:
            try:
                try:
                    timeout = self.recv_queue.get(True, 2.0)
                except Empty:
                    timeout = 1.0
                try:
                    responses = ''
                    response = ''
                    self.__socket.settimeout(timeout)
                    while True:
                        response += (self.__socket.recv(0x4000))
                        if len(select.select([self.__socket], [], [], 0)[0]) == 0:
                            responses += response
                            response = ''
                except socket.timeout:
                #A timeout means there really is nothing left
                #so the response is complete
                    #Just need to 'normalise' the responses
                    #in case there's more than one in there
                    if responses != '':
                        responses = '[' + responses.replace('}\n{',
                                    '},{').replace('}{',
                                    '},{').replace('}[',
                                    '},[').replace(']{',
                                    '],{').replace('][',
                                    '],[') + ']'
                        self.emit("xbmc_received", responses)
                except socket.error:
                    print 'Not connected'
            except Exception as ex:
                print 'Reveiver error: ', ex

