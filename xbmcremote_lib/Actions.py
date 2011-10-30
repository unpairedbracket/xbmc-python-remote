'''
Created on Aug 17, 2011

@author: benspiers
'''

import socket
import select
import XBMCJsonObjects as XJ
import JSONDecoder as decoder

class Actions(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

        #create an INET, STREAMing socket
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def getSocket(self, IpAddress, Port):
        
        #now connect
        self.__s.connect((IpAddress, Port))
        
    def closeSocket(self):
        
        self.__s.shutdown(socket.SHUT_RDWR)
        self.__s.close()
    

    
    def PlayPause(self):
        
        action = XJ.XBMC_PLAY
        return decoder.decodeAnnouncement(self.__sendJson(action))
                
    def PlayNext(self):
        
        action = XJ.XBMC_NEXT
        return decoder.decodeAnnouncement(self.__sendJson(action))
                
    def PlayPrevious(self):
        
        action = XJ.XBMC_PREV
        return decoder.decodeAnnouncement(self.__sendJson(action))
                
    def StartPlaying(self):
        
        action = XJ.XBMC_START
        return decoder.decodeAnnouncement(self.__sendJson(action, 1.0))
                
    def StopPlaying(self):
        
        action = XJ.XBMC_STOP
        return decoder.decodeAnnouncement(self.__sendJson(action))
    
    def GetArtists(self):
        
        action = XJ.GetArtists()
        artistlist = self.__sendJson(action, 0.5)
        artists = ["".join(artistlist)]
        return decoder.decodeResponse(artists)
    
    def GetAlbums(self, artistid=-1):
        
        action = XJ.GetAlbums(artistid)
        albumlist = self.__sendJson(action, 0.5)
        albums = ["".join(albumlist)]
        return decoder.decodeResponse(albums)
    
    def GetSongs(self, artistid=-1, albumid=-1):
        
        action = XJ.GetSongs(artistid, albumid)
        songlist = self.__sendJson(action, 0.5)
        songs = ["".join(songlist)]
        return decoder.decodeResponse(songs)
    
    def checkState(self):
        
        action = XJ.XBMC_STATE
        return decoder.decodeResponse(self.__sendJson(action))
                  
    def sendCustomRequest(self, method, params = {}, announcement=True):
        
        action = XJ.buildJson(method, params, 'custom')
        if announcement:
            return decoder.decodeAnnouncement(self.__sendJson(action))
        else:
            return decoder.decodeResponse(self.__sendJson(action))
                  
    def __sendJson(self, JsonObject, timeout=0.1):

        action = JsonObject
        self.__s.send(action)
        #Some functions take unusually long to respond to
        self.__s.settimeout(timeout)
        responses = []
        while True:
            try: 
                responses.append(self.__returnResponse())
            except socket.timeout:
                return responses
                
    def __returnResponse(self):    
        response = ""
        # Print the results
        while True:
            response += (self.__s.recv(0x4000))
    
            if len(select.select([self.__s], [], [], 0)[0]) == 0:
                return response;
