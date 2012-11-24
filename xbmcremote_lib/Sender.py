import socket
import threading
import asyncore
from asynchat import async_chat

from xbmcremote_lib.XbmcRemoteObject import XbmcRemoteObject

class Sender(async_chat, XbmcRemoteObject):

    def __init__(self, controller):
        XbmcRemoteObject.__init__(self, controller)
        async_chat.__init__(self)
        self.running = False
        self.set_terminator(None)
        self.inbuffer = ''
        self.signal_connect('xbmc_init', self.first_connect)
        self.signal_connect('xbmc_reconnect', self.reconnect)
        self.signal_connect('xbmc_connected', self.start)
        self.signal_connect('xbmc_send', self.add)
        self.signal_connect('xbmc_kill', self.kill)
        self.set_up_thread()

    @property
    def connected(self):
        return self.state['connected']

    @connected.setter
    def connected(self, data):
        self.state['connected'] = data

    def set_up_thread(self):
        self.thread = threading.Thread(target=self.loop, name='Sender Thread')
        self.thread.daemon = True

    @staticmethod
    def tuple_replace(string, old_tuple, new_tuple):
        for old, new in zip(old_tuple, new_tuple):
            string = string.replace(old, new)
        return string

    def collect_incoming_data(self, data):
        self.logger.debug('collected data')
        self.inbuffer = self.inbuffer + data
        if self.inbuffer.count('{') == self.inbuffer.count('}'):
            old = ('}\n{', '}{', '][', ']{', '}[')
            new = ('},{', '},{', '],[', '],{', '},[')
            self.response = '['+self.tuple_replace(self.inbuffer, old, new)+']'
            self.emit('xbmc_received', self.response)
            self.inbuffer = ''

    def get_address(self):
        self.state['ip'] = self.settings.get_string('ip-address')
        self.state['port'] = int(self.settings.get_string('port'))
        return (self.state['ip'], self.state['port'])

    def reconnect(self, signaller, data=None):
        address = self.get_address()
        if ((address != self.addr) or (not self.connected)):
            self.create_and_connect(address)
        else:
            self.emit('xbmc_connected')

    def first_connect(self, signaller, data=None):
        address = self.get_address()
        self.create_and_connect(address)

    def create_and_connect(self, address):
        self._map.clear()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect(address)
        except socket.error:
            self.connected = False
            self.emit('xbmc_disconnected')
        else:
            self.addr = address
            sock.setblocking(0)
            self.set_socket(sock)
            self.start(None)
            self.connected = True
            self.emit('xbmc_connected')

    def loop(self):
        self.running = True
        self.logger.debug('starting looping')
        asyncore.loop(5)
        self.logger.debug('finished looping')
        self.running = False
        self.set_up_thread()            

    def add(self, signaller, request, data=None):
        self.push(request)

    def start(self, signaller, data=None):
        if not self.running:
            self.logger.debug('starting')
            self.thread.start()

    def handle_connect(self):
        self.emit('xbmc_connected')
        self.connected = True

    def handle_close(self):
        self.emit('xbmc_disconnected')
        self.connected = False

    def kill(self, signaller, data=None):
        pass
