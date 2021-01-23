#!/usr/bin/env python

import scraper


sources = [
    scraper.Aftonbladet(),
    scraper.Expressen(),
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

    for header in scrp.headers()[:3]:
        print(header)
        print("")
