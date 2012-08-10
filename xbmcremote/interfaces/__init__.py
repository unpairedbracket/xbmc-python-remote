from xbmcremote_lib.XbmcRemoteObject import XbmcRemoteObject
from threading import Thread
from ast import literal_eval

class BaseInterface(XbmcRemoteObject):

    def __init__(self, application):
        XbmcRemoteObject.__init__(self, application)
        self.methods = {}
        self.connect('xbmc_error', self.handle_error)
        self.connect('xbmc_interface_init', self.thread_loop)
        self.connect('xbmc_response', self.use_response)
        self.connect('xbmc_paused', self.paused)

    def use_response(self, signaller, method, response, data=None):
        if method in self.methods:
            self.methods[method](literal_eval(response))

    def refresh(self, try_connect=True):
        '''
        Override this to refresh the interface before starting its main loop.
        If False is passed to try_connect you should not try to connect using
        the Controller object to avoid infinite loops
        '''
        pass

    def handle_error(self, signaller, message, code, identifier, data=None):
        print 'Error ' + str(code) + ': ' + message

    def show(self):
        '''
        Override this to show a window if there is one, using Gtk.Window.show(), 
        or bring the terminal window to the foreground if there is one of those.
        '''
        pass

    def thread_loop(self, signaller, data=None):
        name = self.__class__.__name__
        self.loop = Thread(target=self.start_loop, name=name+' thread')
        #self.loop.daemon = True
        self.loop.start()

    def start_loop(self):
        '''
        Override this and start the main loop of the Interface, using Gtk.main()
        for gtk windows or some kind of interactive loop for terminal interfaces.
        ''' 
        pass

    def paused(self, signaller, paused, data=None):
        pass
