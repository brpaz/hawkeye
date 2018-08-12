""" Default view, uses a Webview """

from markdown import Markdown
from urllib.parse import urlparse
from urllib.request import urlopen
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, Gdk, WebKit2 as webkit


class MarkdownViewer(webkit.WebView):
    """ Displays the file inside a webview """

    def __init__(self, uri):
        """ constructor """
        super(MarkdownViewer, self).__init__()

        md_string = urlopen(uri).read().decode('utf-8')

        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ], output_format="html5")

        html = md.convert(md_string)

        self.load_html(html, '')
        self.show_all()
