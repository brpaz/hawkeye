""" Default view, uses a Webview """

from markdown import Markdown
from urllib.parse import urlparse
from urllib.request import urlopen
import gi
import os

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import GObject, Gtk, Gdk, Gio, WebKit2 as WebKit
from hawkeye import helpers

class MarkdownViewer(Gtk.VBox):
    """ Displays the file inside a webview """

    __gsignals__ = {
        'external-naviagtion': (GObject.SIGNAL_RUN_LAST, None,
                                ())
    }

    def __init__(self, uri):
        """ constructor """
        super(MarkdownViewer, self).__init__()

        self.webview = WebKit.WebView()
        self.build_search_bar()
        
        settings = self.webview.get_settings()
        settings.set_property('enable-developer-extras', True)

        self.load_assets()

        md_string = urlopen(uri).read().decode('utf-8')

        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ], output_format="html5")

        html = md.convert(md_string)

        self.webview.connect("decide-policy", self.on_decide_policy)

        self.webview.load_html(html, '')
        self.webview.show_all()
        self.pack_start(self.search_bar, False, False, 0)
        self.pack_start(self.webview, True, True, 0)
        self.show_all()

        self.connect("key-press-event", self.on_key_pressed)

    def on_key_pressed(self, widget, event):
        """ Signal called on a key press inside of the main view """
        
        accel_mask = Gtk.accelerator_get_default_mod_mask()

        # Show finder search bar on CTRL-F
        # TODO this should be moved to Main window.
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_f:
          if self.search_bar.get_search_mode():
            self.search_bar.set_search_mode(False)
            self.search_entry.set_text("")
          else:
            self.search_bar.set_search_mode(True)


    def build_search_bar(self):
        """ Builds the search bar widget """
        self.search_bar = Gtk.SearchBar()
        self.search_entry = Gtk.SearchEntry(max_width_chars=45)
        self.search_entry.connect("key-press-event", self.on_search)
        self.search_bar.set_search_mode(False)
        self.search_bar.connect_entry(self.search_entry)
        self.search_bar.add(self.search_entry)
        self.search_bar.set_show_close_button(True)

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

        with open(os.path.join(helpers.Helpers.get_assets_path(), 'css', 'markdown.css'), encoding='utf-8') as f:
            style_contents = f.read()

        with open(os.path.join(helpers.Helpers.get_assets_path(), 'js', 'hljs.js'), encoding='utf-8') as f:
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
        # This behaviour might change, after more time using this on daily basis.
        if decision_type == WebKit.PolicyDecisionType.NAVIGATION_ACTION:
            Gio.AppInfo.launch_default_for_uri(
                decision.get_request().get_uri())
            self.emit('external-naviagtion')
            return decision.ignore()
