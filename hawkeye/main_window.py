
""" hawkeye """

import os
import gi
import sys
import logging
from gi.repository import Gtk, Gdk, Gio

from hawkeye.views.pdf import PdfViewer
from hawkeye.views.markdown import MarkdownViewer
from hawkeye.views.default import DefaultViewer

gi.require_version('Gtk', '3.0')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class MainWindow(Gtk.Window):
    """ Main window for the application """

    def __init__(self, options):
        """ Constructor method """
        super(MainWindow, self).__init__()
        self.logger = logging.getLogger()

        self.logger.info("Launching application")

        self.build_ui(options)
        self.connect_signals()

    def build_ui(self, options={}):
        """ Function that creates the base UI of the application """

        self.set_title("hawkeye")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(options.top)
        self.set_default_size(options.width, options.height)
        self.set_skip_taskbar_hint(True)
        # This hides, minimize and maximize buttons.
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "Hawkeye"

        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        self.hb.pack_end(button)

        self.set_titlebar(self.hb)

        self.scrolled_window = Gtk.ScrolledWindow()

        view = self.build_file_viewer(options.uri)

        self.scrolled_window.add(view)

        self.add(self.scrolled_window)

    def connect_signals(self):
        """ Register event handlers """
        self.connect("key-press-event", self.on_key_pressed)

    def build_file_viewer(self, uri):
        """ Builds the view based on the file type """
        ext = os.path.splitext(uri)[-1].lower()

        if ext == ".pdf":
            self.logger.info("Opening Preview of PDF file")
            return PdfViewer(uri)

        if ext == ".md":
            return MarkdownViewer(uri)

        return DefaultViewer(uri)

    def on_key_pressed(self, widget, event):
        """ handles key press events """

        # close the application on "ESC" key
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

    def open_on_default_app(self, uri):
        """ Opens the file in the default application """

        # Use glib.show_uri
        # This function can be called from hotkey or add a bottom bar menu.
        pass
