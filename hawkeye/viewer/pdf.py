""" Default view, uses a Webview """

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('EvinceView', '3.0')
gi.require_version('EvinceDocument', '3.0')

from gi.repository import Gtk, Gdk, Gio, EvinceDocument, EvinceView, GObject


class PdfViewer(EvinceView.View):
    """ Displays a PDF file using Evince """

    __gsignals__ = {
        'external-naviagtion': (GObject.SIGNAL_RUN_LAST, None,
                                ())
    }

    def __init__(self, uri):
        """ constructor """
        super(PdfViewer, self).__init__()
        self.uri = uri
        self.build_view()

    def build_view(self):
        """ Builds the PDF document """

        EvinceDocument.init()
        self.doc = EvinceDocument.Document.factory_get_document(self.uri)

        model = EvinceView.DocumentModel()
        model.set_document(self.doc)

        self.connect("external-link", self.on_external_link)
        self.connect("key-press-event", self.on_key_pressed)
        self.set_model(model)
        self.show_all()

    def on_key_pressed(self, widget, event):
        """ handles key press events """

        accel_mask = Gtk.accelerator_get_default_mod_mask()

        # Enable copy of text on CTRL-C
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_c:
            widget.copy()

    def on_external_link(self, widget, event):
        """ Handles click on links on PDF files """
        Gio.AppInfo.launch_default_for_uri(event.get_uri())
        self.emit('external-naviagtion')
