# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Ben Spiers 
# This program is free software: you can redistribute it and/or modify it 
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

'''
Package contains the SoundMenu frontend. It doesn't work with TextFrontend
as it causes raw_input to hang
'''
# pylint: disable=R0904
from xbmcremote.frontends import BaseFrontend
from soundmenu import SoundMenuControls


class SoundMenuFrontend(BaseFrontend, SoundMenuControls):

    '''
    The Sound Menu frontend is used to integrate with MPRIS2 compliant sound
    menus such as Ubuntu Unity's sound menu indicator and some Gnome Shell
    extensions.
    '''

    def __init__(self, application):
        BaseFrontend.__init__(self, application)
        self.methods = {'now_playing': self.update_now_playing} 
        SoundMenuControls.__init__(self, 'xbmcremote')

    def _sound_menu_play(self):
        self.emit("xbmc_control", "play", None)

    _sound_menu_pause = _sound_menu_play

    def _sound_menu_next(self):
        self.emit("xbmc_control", "next", None)

    def _sound_menu_previous(self):
        self.emit("xbmc_control", "prev", None)

    def _sound_menu_is_playing(self):
        return not self.state['paused']

    def _sound_menu_raise(self):
        pass

    def paused(self, signaller, paused, data=None):
        if paused:
            self.signal_paused()
        else:
            self.signal_playing()

    def update_now_playing(self, song_info):
        '''Updates the song info in the menu'''
        self.song_changed(song_info['item']['artist'],
                          song_info['item']['album'],
                          song_info['item']['title'])
        #self.signal_playing()
        self.paused(None, self.state['paused'])
