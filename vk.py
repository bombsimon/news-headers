import requests
import header


class VK(header.Reader):
    """
    VK implements a reader for https://vk.se
    """

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

    @classmethod
    def source(cls):
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
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "5690660d118b41a6e129d39fabdfab2c52ed61325d15813825094fbf9f5d0ba0",
                }
            },
        }

        response = requests.post(
            "https://content.vk.se/news/vk/graphql",
            headers={"Content-Type": "application/json"},
            json=body,
        )

        return response.json()
