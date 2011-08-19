'''
Created on Aug 17, 2011

@author: benspiers
'''

class Actions(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        return
    
    def getSocket(self, IpAddress, Port):
        
        import socket
        #create an INET, STREAMing socket
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        #now connect
        self.__s.connect((IpAddress, Port))
        
    def closeSocket(self):
        
        import socket

        self.__s.shutdown(socket.SHUT_RDWR)
        self.__s.close()
    

    
    def PlayPause(self):
        
        from XBMCJson import XBMCJson

        XJ = XBMCJson()

        action = XJ.XBMC_PLAY
        self.__sendJson(action)
                
    def PlayNext(self):
        
        from XBMCJson import XBMCJson

        XJ = XBMCJson()

        action = XJ.XBMC_NEXT
        self.__sendJson(action)
                
    def PlayPrevious(self):
        
        from XBMCJson import XBMCJson

        XJ = XBMCJson()

        action = XJ.XBMC_PREV
        self.__sendJson(action)
                
    def StartPlaying(self):
        
        from XBMCJson import XBMCJson

        XJ = XBMCJson()

        action = XJ.XBMC_START
        self.__sendJson(action)
                
    def StopPlaying(self):
        
        from XBMCJson import XBMCJson

        XJ = XBMCJson()

        action = XJ.XBMC_STOP
        self.__sendJson(action)
                
    def __sendJson(self, JsonObject):
        import select

        action = JsonObject
        self.__s.send(bytes(action, 'UTF-8'))

        # Print the results
        while True:
            response = self.__s.recv(0x4000).decode('UTF-8')
            print(response)
    
            if len(select.select([self.__s], [], [], 0)[0]) == 0:
                break;
                
            