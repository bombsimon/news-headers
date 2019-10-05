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
            title = article.h2
            text =  article.p
            href = article.a

            if title is None:
                continue

            result.append(
                header.Header(
                    " ".join(title.get_text().split()),
                    " ".join(text.get_text().split()),
                    "{}{}".format(self.url(), href.get("href")),
                    False,
                )
            )

        return result
