# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Ben Spiers # This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from xbmcremote.interfaces import BaseInterface
from soundmenu import SoundMenuControls

class SoundMenuInterface(BaseInterface):

    def __init__(self, controller):
        BaseInterface.__init__(self, controller)

        self.sound_menu = SoundMenuControls('xbmcremote')
        self.sound_menu._sound_menu_next = self.play_next
        self.sound_menu._sound_menu_previous = self.play_prev
        self.sound_menu._sound_menu_pause = self.sound_menu._sound_menu_play = self.play_pause
        self.sound_menu._sound_menu_is_playing = self.controller.is_playing

        self.connect("xbmc_new_playing", self.update_now_playing)

    def update_now_playing(self, signaller, artist=None, album=None, title=None, data=None):
        print artist, album, title
        self.sound_menu.song_changed(artist, album, title)
        self.sound_menu.signal_playing()
        self.send_signal(self.controller.paused)

    def play_pause(self):
        self.emit("xbmc_control", "play", None)

    def play_next(self):
        self.emit("xbmc_control", "next", None)

    def play_prev(self):
        self.emit("xbmc_control", "prev", None)

    def send_signal(self, paused):
        if paused:
            self.sound_menu.signal_paused()
        else:
            self.sound_menu.signal_playing()


