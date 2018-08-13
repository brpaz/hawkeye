
""" hawkeye """

import os
import gi
import sys
import logging
from gi.repository import Gtk, Gdk, Gio

from hawkeye.viewer.pdf import PdfViewer
from hawkeye.viewer.markdown import MarkdownViewer
from hawkeye.viewer.default import DefaultViewer

gi.require_version('Gtk', '3.0')

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class MainWindow(Gtk.Window):
    """ Main window for the application """

    def __init__(self, options):
        """ Constructor method """
        super(MainWindow, self).__init__()
        self.logger = logging.getLogger(__name__)
        self.options = options

        self.logger.info("Launching application with options: %s" % options)

        self.build_ui(options)
        self.connect_signals()

    def build_ui(self, options):
        """ Function that creates the base UI of the application """

        self.set_title("Hawkeye")
        self.set_icon_from_file(os.path.dirname(
            __file__) + "/../assets/icon.png")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_keep_above(options.top)
        self.set_default_size(options.width, options.height)
        self.set_skip_taskbar_hint(True)

        # header bar
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "Hawkeye"

        self.btn_open_default = Gtk.Button()
        self.btn_open_default.set_label("Open in Default Application")
        self.hb.pack_end(self.btn_open_default)
        self.set_titlebar(self.hb)

        # viewer that will display the file.
        self.viewer = self.build_file_viewer(options.uri)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.add(self.viewer)

        self.add(self.scrolled_window)

    def connect_signals(self):
        """ Register event handlers """
        self.connect("key-press-event", self.on_key_press)
        self.btn_open_default.connect(
            "button-press-event", self.on_open_in_default_app_btn_pressed)
        # when navigating out of the previewer, close the application
        self.viewer.connect("external-naviagtion",
                            self.on_viewer_external_navigation)

    def build_file_viewer(self, uri):
        """ Builds the view based on the file type """
        ext = os.path.splitext(uri)[-1].lower()

        if ext == ".pdf":
            self.logger.info("Opening file %s using PDF viewer", uri)
            return PdfViewer(uri)

        if ext == ".md":
            self.logger.info("Opening File %s using Markdown Viewer", uri)
            return MarkdownViewer(uri)

        self.logger.info("Opening File %s using Default Viewer", uri)
        return DefaultViewer(uri)

    def on_key_press(self, widget, event):
        """ handles key press events """

        # close the application on "ESC" key
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

    def on_open_in_default_app_btn_pressed(self, widget, event):
        """ Function executed when the user clicks on the "open with default application" button """
        Gio.AppInfo.launch_default_for_uri(self.options.uri)
        self.destroy()

    def on_viewer_external_navigation(self, widget):
        """ Handler for navigation events inside the viewer (Ex: click on external links) """
        self.destroy()
