import gi

gi.require_version('Gtk', '3.0')
gi.require_version('EvinceView', '3.0')
gi.require_version('EvinceDocument', '3.0')

from gi.repository import Gtk, Gdk, Gio

class SearchBar(Gtk.SearchBar):
    """ Top search bar widget """

    def __init__(self):
        """ Init method """
        super(Gtk.SearchBar, self).__init__()
        self.search_entry = Gtk.SearchEntry(max_width_chars=45)

        self.set_search_mode(False)
        self.connect_entry(self.search_entry)
        self.add(self.search_entry)
        self.set_show_close_button(True)

    def set_key_press_handler(self, handler):
        """ Sets the callback that will handle the "key-press-event" on the search widget """
        self.search_entry.connect("key-press-event", handler)
