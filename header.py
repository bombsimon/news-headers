#!/usr/bin/env python3
"""
This module implements a news paper reader and it's headers to support reading
the news text based.
"""

import webbrowser
import requests
import dn


class Header:
    """
    Header is a news header scraped from the news site.
    """

    def __init__(self, title, text, url, premium=False):
        self.title = title
        self.text = text
        self.url = url
        self.premium = premium

    def open_url(self):
        """
        Open a header in the system's configured webbrowser.
        """
        webbrowser.open_new_tab(self.url)


class Reader:
    """
    Reader is the base class to extend to implement a new news site.
    """

    def __init__(self):
        pass

    def url(self):
        raise NotImplementedError

    def headers(self):
        raise NotImplementedError

    def source(self):
        url_source = requests.get(self.url())

        return url_source.text

    def print_cli(self):
        result = self.headers()

        for header in result:
            print("{} {}".format(header.title, "💰" if header.premium else ""))

            if header.text:
                print(header.text)

            print(header.url)

            print()


def main():
    dn.DN().print_cli()


if __name__ == "__main__":
    main()
