#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
import random
import requests


class Aftonbladet:
    def __init__(self):
        self.base_url = "https://aftonbladet.se"

    def url(self):
        return self.base_url

    def headers(self, source):
        soup = BeautifulSoup(source, "html.parser")
        tag_strip = "window.FLUX_STATE = "
        script_tag = ""

        for tag in soup.find_all("script"):
            # Skip empty tags
            if len(tag.contents) < 1:
                continue

            if str.startswith(str(tag.contents[0]), tag_strip):
                script_tag = tag.contents[0][len(tag_strip) :]
                break

        c = json.loads(script_tag)

        articles = c["collections"]
        random_key = list(articles.keys())[0]

        # Always one key - randomized
        contents = articles[random_key]["contents"]
        items = contents["items"]

        result = []

        for item_id, item in items.items():
            # No more articles
            if "abse" not in item_id:
                break

            for i in item["items"]:
                if i["type"] != "teaser":
                    continue

                if "text" not in i:
                    continue

                r = {"title": i["title"]["value"], "text": i["text"]["value"]}

                if i["target"]["type"] == "link:internal":
                    r["url"] = i["target"]["expandedUri"]
                else:
                    r["url"] = i["target"]["uri"]

                result.append(r)

        return result


class DN:
    def __init__(self):
        self.base_url = "https://dn.se"


class Expressen:
    def __init__(self):
        self.base_url = "https://expressen.se"


class Reader:
    def headers(self):
        ab = Aftonbladet()
        ah = ab.headers(self.source(ab.url()))

        rnd = random.choice(ah)
        print(rnd.get("title"))
        print(rnd.get("text"))
        print(rnd.get("url"))

    def source(self, url):
        r = requests.get(url)

        return r.text


if __name__ == "__main__":
    r = Reader().headers()
