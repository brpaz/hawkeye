""" Default view, uses a Webview """

import gi
from gi.repository import GObject, Gtk, Gdk, WebKit2 as webkit

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')


class DefaultViewer(webkit.WebView):
    """ Displays the file inside a webview. This is the default behaviour """

    __gsignals__ = {
        'external-naviagtion': (GObject.SIGNAL_RUN_LAST, None,
                                ())
    }

    def __init__(self, uri):
        """ constructor """
        super().__init__()

        websettings = self.get_settings()
        websettings.set_allow_modal_dialogs(False)
        websettings.set_property("enable-plugins", True)
        websettings.set_property("enable-java", False)
        websettings.set_zoom_text_only(False)

        self.load_uri(uri)
        self.connect('scroll-event', self.on_scroll)

    def on_scroll(self, widget, event):
        """ handles on scroll event"""

        # Handles zoom in / zoom out on Ctrl+mouse wheel
        accel_mask = Gtk.accelerator_get_default_mod_mask()
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK:
            direction = event.get_scroll_deltas()[2]
            if direction > 0:  # scrolling down -> zoom out
                self.set_zoom_level(self.get_zoom_level() - 0.1)
            else:
                self.set_zoom_level(self.get_zoom_level() + 0.1)
