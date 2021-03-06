# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Ben Spiers 
# 
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
Dialog that displays errors.
'''

from gi.repository import Gtk

from xbmcremote_lib.helpers import get_builder

import locale
locale.textdomain('xbmcremote')


class ErrorDialog(Gtk.Dialog): # pylint: disable=W0232

    '''
    ErrorDialog is created by XbmcremoteWindow's handle_error method to
    display an error from the server
    '''

    __gtype_name__ = "ErrorDialog"

    def __new__(cls):
        """
        Special static method that's automatically called by Python when
        constructing a new instance of this class.

        Returns a fully instantiated ErrorDialog object.
        """
        builder = get_builder('ErrorDialog')
        new_object = builder.get_object('error_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """
        Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a ErrorDialog object with it in order to
        finish initializing the start of the new ErrorDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder # pylint: disable=W0201
        self.ui = builder.get_ui(self) # pylint: disable=W0201

    def set_error(self, message, code, identifier=None):
        '''
        Set the error message and identifier if given
        '''
        if identifier is None:
            label = ''.join(['Server-side error ', str(code), ': ', message])
        else:
            label = ''.join(['Server-side error ', str(code), ': ',
                            message, ' (', identifier, ')'])
        self.ui.method_failed_label.set_label(label)

    def on_btn_ok_clicked(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns Gtk.ResponseType.OK from run().
        """
        self.destroy()

def main():
    '''Run the dialog in isolation for testing'''
    dialog = ErrorDialog()
    dialog.show()
    Gtk.main()

if __name__ == "__main__":
    main()
