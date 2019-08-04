from bs4 import BeautifulSoup

import header


class DN(header.Reader):
    @classmethod
    def url(cls):
        """
        The URL for the site.
        """
        return "https://dn.se"

    def headers(self):
        """
        Return a list of all headers for the site.
        """
        soup = BeautifulSoup(self.source(), "html.parser")

        result = []

        for article in soup.find_all("a", class_="teaser"):
            result.append(
                header.Header(
                    " ".join(article.h1.get_text().split()),
                    " ".join(article.p.get_text().split())
                    if article.p is not None
                    else None,
                    "{}{}".format(self.url(), article.get("href")),
                    False,
                )
            )

        return result
