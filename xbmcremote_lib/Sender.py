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

    def set_up_thread(self):
        self.thread = threading.Thread(target=self.loop, name='Sender Thread')
        self.thread.daemon = True

    def collect_incoming_data(self, data):
        self.logger.debug('collected data')
        self.inbuffer = self.inbuffer + data
        if self.inbuffer.count('{') == self.inbuffer.count('}'):
            self.response =  '[' + self.inbuffer.replace('}\n{',
                            '},{').replace('}{',
                            '},{').replace('}[',
                            '},[').replace(']{',
                            '],{').replace('][',
                            '],[') + ']'
            self.emit('xbmc_received', self.response)
            self.inbuffer = ''

    def found_terminator(self):
        pass

    def reconnect(self, signaller, data=None):
        ip = self.state['ip'] = self.settings.get_string('ip-address')
        port = self.state['port'] = int(self.settings.get_string('port'))
        address = (ip, port)
        connected = self.state['connected']
        self.logger.debug('Currently connected to '+str(self.addr)+', going to connect to '+str(address))
        self.logger.debug(self.state['connected'])
        if ((address != self.addr) or (not connected)):
            self.create_and_connect(address)

    def first_connect(self, signaller, data=None):
        ip = self.state['ip'] = self.settings.get_string('ip-address')
        port = self.state['port'] = int(self.settings.get_string('port'))
        address = (ip, port)
        self.create_and_connect(address)

    def create_and_connect(self, address):
        print 'creating socket'
        self._map.clear()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        print sock
        try:
            sock.connect(address)
        except socket.error:
            self.emit('xbmc_disconnected')
            self.state['connected'] = False
        else:
            self.addr = address
            self.emit('xbmc_connected')
            self.state['connected'] = True
            sock.setblocking(0)
            self.set_socket(sock)
            self.start(None)

    def loop(self):
        self.running = True
        print 'starting looping'
        asyncore.loop(5)
        print 'finished looping'
        self.running = False
        self.set_up_thread()            

    def add(self, signaller, request, data=None):
        self.logger.debug('pushing'+request)
        self.push(request)

    def start(self, signaller, data=None):
        if not self.running:
            self.logger.debug('starting')
            self.thread.start()

    def handle_connect(self):
        self.emit('xbmc_connected')
        self.state['connected'] = True

    def handle_close(self):
        self.emit('xbmc_disconnected')
        self.state['connected'] = False

    def kill(self, signaller, data=None):
        pass
