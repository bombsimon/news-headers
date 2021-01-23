# News headers

Scrape Swedish news sites to get the headers. All methods allowed, currently
including DOM parsing, using GraphQL, parsing `<script>` tags and more. :)

* [Aftonbladet](https://aftonbladet.se)
* [DN](https://dn.se)
* [Expressen](https://expressen.se)
* [Fragbite](https://fragbite.se/)
* [SVT](https://svt.se)
* [VK](https://vk.se)*

*\* Must be initialized with a sha256 hash*

## Example usage

```python
>> from scraper import Aftonbladet, SVT
>>> s = SVT()
>>> headers = s.headers()
>>> print(headers[0])
Dödsfall som kopplas till e-cigg ökar – ny studie analyserar skadorna
Forskare: Som att utsättas för senapsgas
https://svt.se/nyheter/utrikes/antal-dodsfall-kopplade-till-e-cigg-okar

>>> a = Aftonbladet()
>>> headers = a.headers()
>>> print(headers[5])
Varför ska vi amma för att rädda klimatet?
Öhagen Britterna kan väl sluta dricka te i stället
https://www.aftonbladet.se/family/a/P9w4Q5/varfor-ska-vi-amma-for-att-radda-klimatet

>>> headers[3].title
Stänger alla butiker – och ger ledigt för fest

>>> headers[3].url
https://www.aftonbladet.se/nyheter/a/vQygkp/jysk-ger-alla-anstallda-ledigt--dagen-efter-personalfest
```

## Implement new sub class

Just extend the `Reader` and implement `name`, `url` and `headers`.

```python
import header

class MySite(Scraper):
    @classmethod
    def name(cls):
        return "My Site"

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
            header.Header(
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
from scraper import SVT, DN
from watcher import Watcher

scrapers = [SVT(), DN()]
w = Watcher(scrapers, 60)

for a in w.articles():
    print("New article posted!")
    print(a)
```
