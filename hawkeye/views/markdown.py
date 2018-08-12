""" Default view, uses a Webview """

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

import markdown
from urllib.parse import urlparse
from urllib.request import urlopen
from gi.repository import Gtk, Gdk, WebKit2 as webkit


class MarkdownViewer(webkit.WebView):
    """ Displays the file inside a webview """

    def __init__(self, uri):
        """ constructor """
        super(MarkdownViewer, self).__init__()

        parsed_url = urlparse(uri)

        md_string = ""
        if parsed_url.scheme == "file":
            with open(uri, "r") as fd:
                md_string = fd.read().decode('utf-8')
        else:
            md_string = urlopen(uri).read().decode('utf-8')

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ], output_format="html5")
        html = md.convert(md_string)

        self.load_html(html, '')
        self.show_all()
