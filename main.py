#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from hawkeye.main_window import MainWindow


def main():

    # parse options
    parser = argparse.ArgumentParser(description='File previewer')
    parser.add_argument("--uri", help="the file or website to display")
    parser.add_argument("--width", help="the window width", default=1024)
    parser.add_argument("--height", help="the window height", default=768)
    parser.add_argument(
        "--top", help="Indicates if the window should be always on top", default=True)
    parser.add_argument(
        "--position", help="The type of window (centered, right, left, right-fullheight", default="overlay")
    args = parser.parse_args()

    window = MainWindow(args)
    # ask to quit the application when the close button is clicked
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()

    Gtk.main()


if __name__ == '__main__':
    main()
