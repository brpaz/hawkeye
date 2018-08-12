#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from hawkeye.main_window import MainWindow


def main():
    """ Application entrypoint """
    # parse options
    parser = argparse.ArgumentParser(description='Hawkeye')
    parser.add_argument("--uri", required=True,
                        help="the file or website to display")
    parser.add_argument("--width", help="the window width", default=1024)
    parser.add_argument("--height", help="the window height", default=768)
    parser.add_argument(
        "--top", help="Indicates if the window should be always on top", default=True)
    args = parser.parse_args()

    window = MainWindow(args)

    # ask to quit the application when the close button is clicked
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()

    # starts the GUI
    Gtk.main()


main()
