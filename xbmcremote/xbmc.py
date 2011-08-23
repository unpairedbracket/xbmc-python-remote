#! /usr/bin/env python

from xbmcremote_lib.Actions import Actions

def main():
    _MYXBMCADDR = "192.168.0.66"
    _MYXBMCPORT = 9090
    REMOTE = Actions()
    
    REMOTE.getSocket(_MYXBMCADDR, _MYXBMCPORT)
    
    while True:
        command = raw_input("What should I do? ")
        if command == "exit":
            break
        elif command == "next":
            REMOTE.PlayNext()
        elif command == "prev":
            REMOTE.PlayPrevious()
        elif command == "pause" or command == "play":
            REMOTE.PlayPause()
        elif command == "start":
            REMOTE.StartPlaying()
        elif command == "stop":
            REMOTE.StopPlaying()
        else:
            print("Unknown command.")
                    
    REMOTE.closeSocket()
    
if __name__ == "__main__":
    main()
