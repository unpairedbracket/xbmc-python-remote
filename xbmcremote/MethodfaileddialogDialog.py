# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gtk

from xbmcremote_lib.helpers import get_builder

import gettext
from gettext import gettext as _
gettext.textdomain('xbmcremote')

class MethodfaileddialogDialog(gtk.Dialog):
    __gtype_name__ = "MethodfaileddialogDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated MethodfaileddialogDialog object.
        """
        builder = get_builder('MethodfaileddialogDialog')
        new_object = builder.get_object('methodfaileddialog_dialog')
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called when we're finished initializing.

        finish_initalizing should be called after parsing the ui definition
        and creating a MethodfaileddialogDialog object with it in order to
        finish initializing the start of the new MethodfaileddialogDialog
        instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self)

    def on_btn_ok_clicked(self, widget, data=None):
        """The user has elected to save the changes.

        Called before the dialog returns gtk.RESONSE_OK from run().
        """
        pass

    def on_btn_cancel_clicked(self, widget, data=None):
        """The user has elected cancel changes.

        Called before the dialog returns gtk.RESPONSE_CANCEL for run()
        """
        pass


if __name__ == "__main__":
    dialog = MethodfaileddialogDialog()
    dialog.show()
    gtk.main()
