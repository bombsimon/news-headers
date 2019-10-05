# News headers

Scrape Swedish news sites to get the headers. All methods allowed, currently
including DOM parsing, using GraphQL, parsing `<script>` tags and more. :)

* [Aftonbladet](https://aftonbladet.se)
* [DN](https://dn.se)
* [Expressen](https://expressen.se)
* [SVT](https://svt.se)
* [VK](https://vk.se)*

*\* Must be initialized with a sha256 hash*

## Example usage

```python
>>> from svt import SVT
>>> from aftonbladet import Aftonbladet
>>>
>>> scraper = SVT()
>>> headers = scraper.headers()
>>> print(headers[0])
Polisen misstänker hatbrott efter skjutningen i Texas
Utreder dokument • ”Indikerar att det kan röra sig om hatbrott''
https://svt.se/nyheter/utrikes/polisen-misstanker-hatbrott-utreder-dokument
>>>
>>> scraper = Aftonbladet()
>>> headers = scraper.headers()
>>> article = headers[5]
>>> print(article)
Melloartisten har gift sig: Mäktigt
▸ Bröllop för Nano – 12 år efter förlovningen
https://www.aftonbladet.se/nojesbladet/a/wP4G3G/nano-omar-och-frida-blum-har-gift-sig
>>>
>>> article.title
'Melloartisten har gift sig: Mäktigt'
>>> article.url
'https://www.aftonbladet.se/nojesbladet/a/wP4G3G/nano-omar-och-frida-blum-har-gift-sig'
```

## Implement new sub class

Just extend the `Reader` and implement `ùrl` and `headers`.

```python
import header

class MySite(header.Reader):
    @classmethod
    def url(cls):
        """
        The URL for the site.
        """
        return "https://mysite.se"

    def headers(self):
        """
        Return a list of all headers for the site.
        """

        return [
            headers.Header(
                "A Title",
                "A text",
                "https://a-url.se",
                True if "paywall" else False,
            )
        ]
```

## Watcher

A simple watcher is bundled with the repository to make it easier to watch for
new articles in desired scrapers. Example usage:

```python
from svt import SVT
from dn import DN
from watcher import Watcher

scrapers = [SVT(), DN()]
w = Watcher(scrapers, 60)

for a in w.articles():
    print("New article posted!")
    print(a)
```