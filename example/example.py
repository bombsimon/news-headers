#!/usr/bin/env python
"""
This is an example of all the scrapers in action.
"""

import scraper


sources = [
    scraper.Aftonbladet(),
    scraper.Expressen(),
    scraper.Fragbite(),
    scraper.DN(),
    scraper.SVT(),
    scraper.VK(
        "478abbc7153221815eb145e4ae1d2ebe2659aa5147a17ea5ea49b78d44aa17fe"
    ),
]

for scrp in sources:
    print("======================================= ")
    print(" > {}".format(scrp.name()))
    print("======================================= ")

    try:
        for header in scrp.headers()[:3]:
            print(f"{header}\n")
    # pylint: disable=W0702
    # noqa: E722
    except:
        print(
            f"Example not working for {scrp.name()}, it probably needs update\n"
        )
