""" Default view, uses a Webview """

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('EvinceView', '3.0')
gi.require_version('EvinceDocument', '3.0')

from gi.repository import Gtk, Gdk, Gio, EvinceDocument, EvinceView, GObject


class PdfViewer(Gtk.VBox):
    """ Displays a PDF file using Evince """

    __gsignals__ = {
        'external-naviagtion': (GObject.SIGNAL_RUN_LAST, None,
                                ())
    }

    def __init__(self, uri):
        """ constructor """
        super(PdfViewer, self).__init__()
        self.uri = uri
        self.searched_text = ""
        self.find_job = None

        self.build_search_bar()
        self.build_pdf_view()

        self.connect_signals()

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.add(self.view)
        self.pack_start(self.search_bar, False, False, 0)
        self.pack_start(self.scrolled_window, True, True, 0)
        self.show_all()

    def connect_signals(self):
        """ Connect signals """
        self.connect("key-press-event", self.on_key_press)
        self.view.connect("external-link", self.on_link_click)

    def build_pdf_view(self):
        """ Builds the PDF document """

        EvinceDocument.init()
        self.view = EvinceView.View()
        self.doc = EvinceDocument.Document.factory_get_document(self.uri)

        model = EvinceView.DocumentModel()
        model.set_document(self.doc)

        self.view.set_model(model)

    def build_search_bar(self):
        """ builds the SearchBar widget """
        self.search_entry = Gtk.SearchEntry(max_width_chars=45)
        self.search_entry.connect("key-press-event", self.on_search)

        self.search_bar = Gtk.SearchBar()
        self.search_bar.set_search_mode(False)
        self.search_bar.connect_entry(self.search_entry)
        self.search_bar.add(self.search_entry)
        self.search_bar.set_show_close_button(True)

    def on_search(self, widget, event):
        """ Perform a search"""

        # only perform a search when "Enter" key is pressed.
        if event.keyval != Gdk.KEY_Return:
            return

        text = widget.get_text()

        # if the currency text is the same of the previous input search, it means its the same search.
        # it this case, we move to the next result
        if (self.searched_text == text):
            self.view.find_next()
            return

        # its a new search. Create a new find job and execute it.
        self.searched_text = text

        if (self.find_job is not None):
            self.find_job.cancel()
            self.find_job = None

        # dont do a search for empty text.
        if text == "":
            self.view.find_set_highlight_search(False)
            return

        self.find_job = EvinceView.JobFind.new(document=self.doc, start_page=0,
                                        n_pages=self.doc.get_n_pages(),
                                        text=text, case_sensitive=False)

        self.view.find_started(self.find_job)
        EvinceView.Job.scheduler_push_job(self.find_job,
                                    EvinceView.JobPriority.PRIORITY_NONE)

        self.view.find_set_highlight_search(True)

    def on_key_press(self, widget, event):
        """ handles key press events """

        accel_mask = Gtk.accelerator_get_default_mod_mask()

        # Enable copy of text on CTRL-C
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_c:
            widget.copy()

        # Show finder search bar on CTRL-F
        # TODO this should be moved to Main window.
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_f:
            if self.search_bar.get_search_mode():
                self.search_bar.set_search_mode(False)
                self.search_entry.set_text("")
            else:
                self.search_bar.set_search_mode(True)

    def on_link_click(self, widget, event):
        """ Handles click on links on PDF files """
        Gio.AppInfo.launch_default_for_uri(event.get_uri())
        self.emit('external-naviagtion')
