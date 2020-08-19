#!/usr/bin/env python

import scraper


sources = {
    "Aftonbladet": scraper.Aftonbladet(),
    "Expressen": scraper.Expressen(),
    "DN": scraper.DN(),
    "SVT": scraper.SVT(),
    "VK": scraper.VK(
        "478abbc7153221815eb145e4ae1d2ebe2659aa5147a17ea5ea49b78d44aa17fe"
    ),
}

for source_name, scrp in sources.items():
    print("======================================= ")
    print(" > {}".format(source_name))
    print("======================================= ")

    for header in scrp.headers()[:3]:
        print(header)
        print("")
