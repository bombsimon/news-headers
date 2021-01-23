import json
import requests
from bs4 import BeautifulSoup
import header


class Scraper:
    """
    Reader is the base class to extend to implement a new news site.
    """

    def __init__(self):
        pass

    def name(self):
        raise NotImplementedError

    def url(self):
        raise NotImplementedError

    def headers(self):
        raise NotImplementedError

    def source(self):
        url_source = requests.get(self.url())

        return url_source.text

    def print_cli(self):
        headers = self.headers()

        for news_header in headers:
            print(news_header)
            print()


class Aftonbladet(Scraper):
    """
    Aftonbladet implements a reader for https://aftonbladet.se

    Aftonbladet is quite special since all the content of the site that we need
    is located as JSON inside a <script> tag where the variable
    `window.FLUX_STATE` is set to this content.

    By iterating over the <script> tags and looking for the one starting with an
    assignment to this variable we can extract the tag content and just read the
    JSON. When that's done all we need to do is iterate over the data and store
    what's relevant to us.
    """

    SCRIPT_TAG_START = "window.FLUX_STATE = "

    @classmethod
    def name(cls):
        return "Aftonbladet"

    @classmethod
    def url(cls):
        """
        The URL for the site.
        """
        return "https://aftonbladet.se"

    def headers(self):
        """
        Return a list of all headers for the site.
        """
        soup = BeautifulSoup(self.source(), "html.parser")
        script_tag = None

        for tag in soup.find_all("script"):
            # Skip empty tags
            if not tag.contents:
                continue

            # Check if the tag content starts with the JSON assignment.
            if tag.contents[0].startswith(self.SCRIPT_TAG_START):
                script_tag = tag.contents[0][len(self.SCRIPT_TAG_START) :]
                break

        if script_tag is None:
            raise Exception("No tags found")

        json_content = json.loads(script_tag)

        articles = json_content["collections"]

        # Always one key - randomized string.
        random_key = list(articles.keys())[0]
        items = articles[random_key]["contents"]["items"]

        result = []

        for item_id, item in items.items():
            # No more articles if we no longer find the "abse" key.
            if "abse" not in item_id:
                break

            for sub_item in item["items"]:
                # We're looking for teasers to fetch.
                if sub_item["type"] != "box":
                    continue

                if "clickTracking" not in sub_item:
                    continue

                if "object" not in sub_item["clickTracking"]:
                    continue

                if "name" not in sub_item["clickTracking"]["object"]:
                    continue

                title = sub_item["clickTracking"]["object"]["name"]
                text = self._find_text(sub_item)
                link = sub_item["clickTracking"]["target"]["url"]

                result.append(header.Header(title, text, link,))

        return result

    def _find_text(self, item):
        r = self._traverse_items(item, [])
        return r[len(r) - 1]

    def _traverse_items(self, item, found):
        if "text" in item and "value" in item["text"]:
            found.append(item["text"]["value"])

        if "items" in item:
            for i in item["items"]:
                self._traverse_items(i, found)

        return found


class DN(Scraper):
    @classmethod
    def name(cls):
        return "Dagens Nyheter"

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


class Expressen(Scraper):
    """
    Expressen implements a reader for https://expressen.se
    """

    @classmethod
    def name(cls):
        return "Expressen"

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


class SVT(Scraper):
    """
    SVT implements a reader for https://svt.se
    """

    @classmethod
    def name(cls):
        return "Sveriges Television"

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


class VK(Scraper):
    """
    VK implements a reader for https://vk.se. When the site fetches the news
    articles it's made with graphql and a body containing a sha256 hash. I have
    yet to figure out how this is calculated but in the meantime a new instance
    of VK must be created with the hash. The hash can be found by using the
    network inspector in a web browser and looking for a HTTP POST request to
    https://content.vk.se/news/vk/graphql. In the body for that request you
    should find a similar rbody to the one in this file.
    """

    def __init__(self, sha256):
        self.sha256hash = sha256

        super().__init__()

    @classmethod
    def name(cls):
        return "Västerbottens-Kuriren"

    @classmethod
    def url(cls):
        """
        The URL for the site.
        """
        return "https://vk.se"

    def headers(self):
        """
        Return a list of all headers for the site.
        """

        gql = self.source()

        result = []

        for item in gql["data"]["result"]["hits"]:
            teaser = item["teaser"]

            result.append(
                header.Header(
                    teaser["title"],
                    teaser["text"],
                    "{}{}".format(self.url(), item["urlPath"]),
                    item["paywall"] == "premium",
                )
            )

        return result

    def source(self):
        """
        Custom implementation to fetch the source for VK since VK uses GraphQL
        which we may use to fetch the articles.
        """
        body = {
            "operationName": "OCListQueryNonBatched",
            "variables": {
                "uuid": "7a3463a2-988c-43ba-99f3-39f27fe3d265",
                "limit": 100,
                "page": 0,
            },
            "extensions": {
                "persistedQuery": {"version": 1, "sha256Hash": self.sha256hash}
            },
        }

        response = requests.post(
            "https://content.vk.se/news/vk/graphql",
            headers={"Content-Type": "application/json"},
            json=body,
        )

        return response.json()


class Fragbite(Scraper):
    """
    Fragbite implements a reader for fragbite.se
    News title contains number of comments inside "()"
    """

    @classmethod
    def url(cls):
        """
        The URL for the site.
        """
        return "https://fragbite.se"

    @classmethod
    def name(cls):
        return "Fragbite"

    def headers(self):
        """
        Return a list of all headers for the site.
        """
        soup = BeautifulSoup(self.source(), "html.parser")

        result = []

        for article in soup.find_all("div", class_="text"):
            subheading = article.find("div", class_="subheading")

            result.append(
                header.Header(
                    article.h1.get_text(),
                    subheading.get_text(),
                    "{}{}".format(self.url(), article.a.get("href")),
                    False,
                )
            )

        return result
