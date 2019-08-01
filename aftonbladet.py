from bs4 import BeautifulSoup
import json
import header


class Aftonbladet(header.Reader):
    """
    Aftonbladed implements a reader for https://aftonbladet.se

    Aftonbladet is quite special since all the content of the site that we need
    is located as JSON insited a <script> tag where the variable
    `window.FLUX_STATE` is set to this content.

    By iterating over the <script> tags and looking for the one starting with an
    assignment to this variable we can extract the tag content and just read the
    JSON. When that's done all we need to do is iterate over the data and store
    what's relevant to us.
    """

    SCRIPT_TAG_START = "window.FLUX_STATE = "

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
            raise "No tags found"

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
                if sub_item["type"] != "teaser":
                    continue

                # And we require them to have a text.
                if "text" not in sub_item:
                    continue

                result.append(
                    header.Header(
                        sub_item["title"]["value"],
                        sub_item["text"]["value"],
                        sub_item["target"]["expandedUri"]
                        if sub_item["target"]["type"] == "link:internal"
                        else sub_item["target"]["uri"],
                    )
                )

        return result
