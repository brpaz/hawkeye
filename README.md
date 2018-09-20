# Hawkeye

> Hawkeye is a command line GTK Application that allow to quickly open PDFs, Markkown Files, Images and Websites in a "small" window, somewhat inspired by MacOS [quicklook](https://support.apple.com/kb/ph25575?locale=en_US).


[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
![License](https://img.shields.io/github/license/brpaz/hawkeye.svg)
![Requires.io](https://img.shields.io/requires/github/brpaz/hawkeye.svg)

## Motivation

Many times when working, I feel the need to quickly look up some documentation website or cheatsheet, while minimizing the context switching required to open a full web browser or file. Also tradiional browser have many elements like tabs, search bar, extensions, etc that take a lot of space and make it harder to have a full browser window open side by side with your IDE. Besides, I also wanted to be able to "preview" content inside [ulauncher](https://ulauncher.io/) and some extensions I have been working on like [ulauncher-cheat-sheets](https://github.com/brpaz/ulauncher-cheats).

Thats when the idea of Hawkeye come from.

## Main features

* Supports most common file types:
    * PDF files
    * Markdown files
    * Websites / HTML and other web files that can be displayed inside a Webview
* Command line tool makes easy to integrate with other applications.
* Application window contains only the basic elements to display the file making it easy to have windows side by side or on top.
* Search function allows you to search in the displayed content.

## Requirements

* Python 3 (with all the dependencies specified in the [requirements.txt](requirements.txt) file.)
* GTK
* [Evince](https://wiki.gnome.org/Apps/Evince) (for PDF files display)
* GI Evince bindings - install with `sudo apt-get install gir1.2-evince-3`

This was only tested in Ubuntu 18.04 but it should work in other OSes that meets the above requirements.

## Install

For now the only way to install this application is installing from source. I would like to provide flatpak, snap, deb support in the future. If you know how to package Python apps in these formats, PRs are welcome ;)

```make install```

## Usage

From terminal, execute the following command:

```hawkeye --uri="https://google.com"```

Where the uri parameter is the path to the file you want to open.

"http" and "file" protocols are supported. For PDF files only local files are supported.

You can pass additional arguments to the command. type "hawkeye -h" to see the available arguments.

---

## FAQ

### How does Hawkeye compares with gnome-sushi?

* [Gnome sushi](https://github.com/GNOME/sushi) is a quick previewer for Nautilus, the GNOME desktop file manager. It allows to preview the most popular file types just by typing the "space bar" on the file manager and supports many file types. Hawkeye aims for a more specific use case, outside of the file manager scope, where you need to integrate with other apps, thus being a command line tool. Also it is more that a previewer as it allows zooming and searching for example. This project doesnt want to be a replacement to gnome sushi and both can be used togeher for the ultimate killer workflow.


## Contributing

All contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT
