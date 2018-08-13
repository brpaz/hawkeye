# Hawkeye - Linux File Previewer

> GTK Application to quicly preview PDFs, Markkown Files, Images and Websites in a simple window, somewhat inspired by MacOS [quicklook](https://support.apple.com/kb/ph25575?locale=en_US)

## Motivation

Many times when working, I feel the need to quickly look up some documentation website or cheatsheet, while minimizing the context switching required to open a full web browser or file. Also tradiional browser have many elements like tabs, search bar, extensions, etc that take a lot of space and make it harder to have a full browser window open side by side with your IDE. Besides, I also wanted to be able to "preview" content inside [ulauncher](https://ulauncher.io/) and some extensions I have been working on like [ulauncher-cheat-sheets](https://github.com/brpaz/ulauncher-cheat-sheets).

Thats when the idea of Hawkeye come from.

## Main features

* Supports most common file types:
    * PDF files (using Evince),
    * Markdown files,
    * Websites / HTML and other web files that can be displayed inside a Webview.
* Command line tool makes easy to integrate with other applications.
* Application window contains only the basic elements to display the file.

## Requirements

* Python 3 (with all the dependencies specified in the [requirements.txt](requirements.txt) file.)
* GTK
* [Evince](https://wiki.gnome.org/Apps/Evince) (for PDF files display)

## Install

For now only "setup.py" is supported. I would like to provide flatpak, snap, deb support in the future. If you know how to package Python apps in these formats, PRs are welcome ;)

```python setup.py install```

## Usage

From terminal, execute the following command:

```hawkeye --uri="https://google.com"```

Where the uri parameter is the path to the file you want to open.

"http" and "file" protocols are supported. For PDF files only local files are supported.

You can pass additional parameters to the command. type "hawkeye -h" to see the available commands.

## FAQ

### How does hawkeye compares with gnome-sushi?

* [Gnome sushi](https://github.com/GNOME/sushi) is a quick previewer for Nautilus, the GNOME desktop file manager. It allows to preview the most popular file types just by typing the "spacebar" on the file explorer. Hawkeye aims for a more specific use cases, where you need to integrate with other apps, thus being a command line tool. Also it is more that a previewer as it allows zooming for example. This project doesnt want to be a replacement to gnome sushi and both can be used togeher for the ultimate killer workflow.

## TODO

- Markdown preview css (margin, code blocks and colors)
- PDF copy text


## Contributing

All contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT
