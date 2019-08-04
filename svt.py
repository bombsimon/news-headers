from bs4 import BeautifulSoup
import header


class SVT(header.Reader):
    """
    SVT implements a reader for https://svt.se
    """

    @classmethod
    def url(cls):
        """
        The URL for the site.
        """
        return "https://svt.se"

    def headers(self):
        """
        Return a list of all headers for the site.
        """
        soup = BeautifulSoup(self.source(), "html.parser")

        result = []

        for article in soup.find_all("article", class_="nyh_teaser"):
            textwrapper = article.find("div", class_="nyh_teaser__textwrapper")

            result.append(
                header.Header(
                    textwrapper.h1.get_text(),
                    textwrapper.div.get_text(),
                    "{}{}".format(self.url(), article.a.get("href")),
                    False,
                )
            )

        return result
