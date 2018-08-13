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

class MarkdownViewer(WebKit.WebView):
    """ Displays the file inside a webview """

    __gsignals__ = {
        'external-naviagtion': (GObject.SIGNAL_RUN_LAST, None,
                                ())
    }

    def __init__(self, uri):
        """ constructor """
        super(MarkdownViewer, self).__init__()

        settings = self.get_settings()
        settings.set_property('enable-developer-extras', True)

        self.load_assets()

        md_string = urlopen(uri).read().decode('utf-8')

        md = Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br'
        ], output_format="html5")

        html = md.convert(md_string)

        self.connect("decide-policy", self.on_decide_policy)

        self.load_html(html, '')
        self.show_all()

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

        self.get_user_content_manager().add_style_sheet(style)
        self.get_user_content_manager().add_script(script)

    def on_decide_policy(self, webview, decision, decision_type):
        """ Intercepts requests """
        # Always opens external links in external application.
        # This behaviour might change, after more time using this on daily basis.
        if decision_type == WebKit.PolicyDecisionType.NAVIGATION_ACTION:
            Gio.AppInfo.launch_default_for_uri(
                decision.get_request().get_uri())
            self.emit('external-naviagtion')
            return decision.ignore()
