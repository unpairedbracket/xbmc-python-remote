from xbmcremote_lib.XbmcRemoteObject import XbmcRemoteObject

class BaseInterface(XbmcRemoteObject):

    def __init__(self, controller):
        XbmcRemoteObject.__init__(self, controller)
        self.connect('xbmc_get', self.controller.get_data)
        self.connect('xbmc_control', self.controller.send_control)

    def refresh(self, try_connect=True):  
        '''
        Override this to refresh the interface before starting its main loop.
        If False is passed to try_connect you should not try to connect using
        the Controller object to avoid infinite loops
        '''
        if try_connect and not self.controller.connected:
            self.controller.connect_to_xbmc(True)

    def handle_error(self, signaller, message, code, identifier, data=None):
        print 'Error ' + code + ': ' + message

    def show(self):
        '''
        Override this to show a window if there is one, using Gtk.Window.show(), 
        or bring the terminal window to the foreground if there is one of those.
        '''
        pass

    def start_loop(self):
        '''
        Override this and start the main loop of the Interface, using Gtk.main()
        for gtk windows or some kind of interactive loop for terminal interfaces.
        ''' 
        pass

    def paused(self, paused):
        pass
