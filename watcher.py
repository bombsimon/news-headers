"""
This is a watcher that given a list of scrapers will check every X interval forr
new links and yield a new message when that happens.
"""
import time


class Watcher:
    """
    A watcher runs in the background and checks for new links.
    """

    def __init__(self, scrapers=[], interval=60):
        """
        Create a new Watcher.
        """
        self.scrapers = scrapers
        self.interval = interval
        self.seen_articles = {}

        self.init_articles()

    def init_articles(self):
        """
        Init articles will store all current articles in the watcher.
        :return:
        """
        for scraper in self.scrapers:
            headers = scraper.headers()

            for header in headers:
                self.seen_articles[header.url] = header

    def articles(self):
        """
        Articles watches all the news sites and returns a message if new
        articles are posted.
        :return: Yields message
        """

        while True:
            for scraper in self.scrapers:
                headers = scraper.headers()

                for header in headers[0:2]:
                    if header.url not in self.seen_articles:
                        yield header

                    self.seen_articles[header.url] = header

            time.sleep(self.interval)
