import requests
import header


class VK(header.Reader):
    """
    VK implements a reader for https://vk.se. When the site fetches the news
    articles it's made with graphql and a body containing a sha256 hash. I have
    yet to figure out how this is calculated but in the meantime a new intance
    of VK must be created with the hash. The hash can be found by using the
    network inspector in a web browser and looking for a HTTP POST request to
    https://content.vk.se/news/vk/graphql. In the body for that request you
    should find a siilar rbody to the one in this file.
    """

    def __init__(self, sha256):
        self.sha256hash = sha256

        super().__init__()

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
