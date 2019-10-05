from bs4 import BeautifulSoup
import header


class Expressen(header.Reader):
    """
    Expressen implements a reader for https://expressen.se
    """

    @classmethod
    def url(cls):
        """
        The URL for the site.
        """
        return "https://expressen.se"

    def headers(self):
        """
        Return a list of all headers for the site.
        """
        soup = BeautifulSoup(self.source(), "html.parser")

        result = []

        for article in soup.find_all("div", class_="teaser"):
            if article.h2 is None:
                continue

            result.append(
                header.Header(
                    " ".join(article.h2.get_text().split()),
                    " ".join(article.p.get_text().split()),
                    "{}{}".format(self.url(), article.a.get("href")),
                    False,
                )
            )

        return result
