'''
Created on 30 Oct 2011

@author: ben
'''
from json import JSONEncoder, JSONDecoder

encoder = JSONEncoder()
decoder = JSONDecoder()

def decodeAnnouncement(Json):
    #check last first to return the latest valid Announcement message
    for i in reversed(Json):
        try:
            js = decoder.decode(i)
            #check for a valid Announcement
            if js['method'] == 'Announcement':
                message = js['params']['message']
                return {'type': 'announcement', 'data': message}
        except (ValueError, KeyError):
            pass
    return decodeError(Json)

def decodeResponse(Json):
    #check last first to return the latest valid result
    for i in reversed(Json):
        try:
            js = decoder.decode(i)
            #check for a valid response
            if js.has_key(u'error'):
                break
            if js.has_key(u'id'):
                result = js['result']
                return {'type': 'response', 'data': result}
        except ValueError:
            pass
    return decodeError(Json)

def decodeError(Json):
    
    for i in reversed(Json):
        try:
            js = decoder.decode(i)
            #check for an error
            if js.has_key(u'error'):
                result = js['error']
                return {'type': 'error', 'data': result}
        except ValueError:
            pass
    #if nothing found, return empty dictionary
    return {'type': 'none', 'data': {}}