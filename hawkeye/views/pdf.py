""" Default view, uses a Webview """

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('EvinceView', '3.0')
gi.require_version('EvinceDocument', '3.0')

from gi.repository import Gtk, Gdk, EvinceDocument, EvinceView


class PdfViewer(EvinceView.View):
    """ Displays a PDF file using Evince """

    def __init__(self, uri):
        """ constructor """
        super(PdfViewer, self).__init__()
        self.uri = uri
        self.build_view()

    def build_view(self):
        """ Builds the PDF document """
     
        EvinceDocument.init()
        doc = EvinceDocument.Document.factory_get_document(self.uri)

        model = EvinceView.DocumentModel()
        model.set_document(doc)

        # TODO implment copy
        # EvinceView.View.signals.selection_changed
        # https: // lazka.github.io/pgi-docs/EvinceView-3.0/classes/View.html

        self.set_model(model)
        self.show_all()
