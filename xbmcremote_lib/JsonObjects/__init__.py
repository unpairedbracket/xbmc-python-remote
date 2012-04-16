from gi.repository import Gio

settings = Gio.Settings("net.launchpad.xbmcremote")

if settings.get_int('version') == 0:
    import DharmaJsonObjects as XJ
elif settings.get_int('version') == 1:
    import EdenJsonObjects as XJ
