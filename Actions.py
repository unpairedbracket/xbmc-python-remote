'''
Created on Aug 17, 2011

@author: benspiers
'''

import socket
import select

class Actions(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        from XBMCJsonObjects import XBMCJson
        self.XJ = XBMCJson()
        #create an INET, STREAMing socket
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def getSocket(self, IpAddress, Port):
        
        #now connect
        try:
            self.__s.connect((IpAddress, Port))
            return True
        except socket.error:
            return False
        
    def closeSocket(self):
        
        self.__s.shutdown(socket.SHUT_RDWR)
        self.__s.close()
    

    
    def PlayPause(self):
        
        action = self.XJ.XBMC_PLAY
        self.__sendJson(action)
                
    def PlayNext(self):
        
        action = self.XJ.XBMC_NEXT
        self.__sendJson(action)
                
    def PlayPrevious(self):
        
        action = self.XJ.XBMC_PREV
        self.__sendJson(action)
                
    def StartPlaying(self):
        
        action = self.XJ.XBMC_START
        self.__sendJson(action)
                
    def StopPlaying(self):
        
        action = self.XJ.XBMC_STOP
        self.__sendJson(action)
                
    def __sendJson(self, JsonObject):

        action = JsonObject
        self.__s.send(action)

        self.__logResponse()
        
    def __logResponse(self):    
        import logging
        log = logging.getLogger("responses")
        # Print the results
        while True:
            response = self.__s.recv(0x4000)
            log.debug(response)
    
            if len(select.select([self.__s], [], [], 0)[0]) == 0:
                break;
                
    def __returnResponse(self):    
        response = []
        # Print the results
        while True:
            response.append(self.__s.recv(0x4000))
    
            if len(select.select([self.__s], [], [], 0)[0]) == 0:
                return response;
