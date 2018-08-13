""" Default view, uses a Webview """

import os
import gi

from markdown import Markdown
from urllib.request import urlopen

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import GObject, Gtk, Gdk, Gio, WebKit2 as WebKit
from hawkeye.ui.search_bar import SearchBar


class MarkdownViewer(Gtk.VBox):
    """ Displays the file inside a webview """

    __gsignals__ = {
        'external-naviagtion': (GObject.SIGNAL_RUN_LAST, None,
                                ())
    }

    def __init__(self, uri):
        """ constructor """
        super().__init__()

        self.uri = uri
        self.build_ui()
        self.connect_signals()
        self.load_assets()

        html = self.convert_markdown()
        self.webview.load_html(html, '')
        self.show_all()

    def build_ui(self):
        """ Builds the ui widgets """
        self.webview = WebKit.WebView()
        self.search_bar = SearchBar()
        self.search_bar.set_key_press_handler(self.on_search)

        self.pack_start(self.search_bar, False, False, 0)
        self.pack_start(self.webview, True, True, 0)

    def connect_signals(self):
        """ Configure signal handlers """
        self.webview.connect("decide-policy", self.on_decide_policy)
        self.connect("key-press-event", self.on_key_press)

    def convert_markdown(self):
        """ Converts Markdown to HTML """
        md_string = urlopen(self.uri).read().decode('utf-8')

        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ], output_format="html5")

        return md.convert(md_string)

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

    def on_search(self, widget, event):
        """ Do a search on enter key """

        if event.keyval != Gdk.KEY_Return:
            return

        script = """
            var res = window.find("%s")
            if (!res) {
                alert("No results found!")
            }
        """

        script = script % widget.get_text()
        self.webview.run_javascript(script)

    def load_assets(self):
        """ Injects css and js files into the webview """

        assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')

        with open(os.path.join(assets_path, 'css', 'markdown.css'), encoding='utf-8') as f:
            style_contents = f.read()

        with open(os.path.join(assets_path, 'js', 'hljs.js'), encoding='utf-8') as f:
            hljs_script = f.read()

        style = WebKit.UserStyleSheet(
            style_contents, WebKit.UserContentInjectedFrames.TOP_FRAME, WebKit.UserStyleLevel.USER, None, None)

        script = WebKit.UserScript(
            hljs_script, WebKit.UserContentInjectedFrames.TOP_FRAME, WebKit.UserScriptInjectionTime.END, None, None)

        self.webview.get_user_content_manager().add_style_sheet(style)
        self.webview.get_user_content_manager().add_script(script)

    def on_decide_policy(self, webview, decision, decision_type):
        """ Intercepts requests """
        # Always opens external links in external application.
        # This behaviour might change, after more time using this on daily
        # basis.
        if decision_type == WebKit.PolicyDecisionType.NAVIGATION_ACTION:
            Gio.AppInfo.launch_default_for_uri(
                decision.get_request().get_uri())
            self.emit('external-naviagtion')
            return decision.ignore()
