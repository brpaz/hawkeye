""" Default view, uses a Webview """

import gi

from hawkeye.ui.search_bar import SearchBar
from gi.repository import GObject, Gtk, Gdk, WebKit2 as webkit

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')


class DefaultViewer(Gtk.VBox):
    """ Displays the file inside a webview. This is the default behaviour """

    __gsignals__ = {
        'external-naviagtion': (GObject.SIGNAL_RUN_LAST, None,
                                ())
    }

    def __init__(self, uri):
        """ constructor """
        super().__init__()

        self.webview = webkit.WebView()
        websettings = self.webview.get_settings()
        websettings.set_allow_modal_dialogs(False)
        websettings.set_property("enable-plugins", True)
        websettings.set_property("enable-java", False)
        websettings.set_zoom_text_only(False)

        self.search_bar = SearchBar()

        self.search_bar.set_key_press_handler(self.on_search)

        self.pack_start(self.search_bar, False, False, 0)
        self.pack_start(self.webview, True, True, 0)

        self.connect('key-press-event', self.on_key_press)
        self.webview.connect('scroll-event', self.on_scroll)

        # TODO this is not working. (segmentation fault)
        #self.find_controller = webkit.FindController()

        self.webview.load_uri(uri)
        self.show_all()

    def on_key_press(self, widget, event):
        """ Signal called on a key press inside of the main view """

        accel_mask = Gtk.accelerator_get_default_mod_mask()

        # Show finder search bar on CTRL-F
        # TODO this should be moved to Main window.
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_f:
            if self.search_bar.get_search_mode():
                self.search_bar.set_search_mode(False)
                self.search_bar.set_text("")
            else:
                self.search_bar.set_search_mode(True)

    def on_scroll(self, widget, event):
        """ handles on scroll event"""

        # Handles zoom in / zoom out on Ctrl+mouse wheel
        accel_mask = Gtk.accelerator_get_default_mod_mask()
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK:
            direction = event.get_scroll_deltas()[2]
            if direction > 0:  # scrolling down -> zoom out
                self.webview.set_zoom_level(
                    self.webview.get_zoom_level() - 0.1)
            else:
                self.webview.set_zoom_level(
                    self.webview.get_zoom_level() + 0.1)

    def on_search(self, widget, event):
        """ Do a search on enter key """

        if event.keyval != Gdk.KEY_Return or widget.get_text() == "":
            return

        script = """
            var res = window.find("%s", false, false, true, false, false, true)
            if (!res) {
                alert("No results found!")
            }
        """

        script = script % widget.get_text()
        self.webview.run_javascript(script)
