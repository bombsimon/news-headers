#!/usr/bin/env python3
"""
This module implements a news paper reader and it's headers to support reading
the news text based.
"""

import webbrowser


class Header:
    """
    Header is a news header scraped from the news site.
    """

    def __init__(self, title, text, url, premium=False):
        self.title = title
        self.text = text
        self.url = url
        self.premium = premium

    def __str__(self):
        header = ["{} {}".format(self.title, "💰" if self.premium else "")]

        if self.text:
            header.append(self.text)

        header.append(self.url)

        return "\n".join(header)

    def open_url(self):
        """
        Open a header in the system's configured webbrowser.
        """
        webbrowser.open_new_tab(self.url)
