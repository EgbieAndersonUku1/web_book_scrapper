import requests

from bs4 import BeautifulSoup
from web_book_scrapper.menu.menu_parser import MenuParser
from web_book_scrapper.products.product_parser import ProductParser


class BooksToScrapePage(object):

    def __init__(self, url):
        self.url = url
        self._soup_handler = None

    def initalize(self):
        """Initialise the class. This must be run before any off the properties are called"""
        page = requests.get(self.url)
        if page:
            self._soup_handler = BeautifulSoup(page.content, "html.parser")
           
    @property
    def menu(self):
        """Returns a list of menu categories found on the page"""
        return MenuParser(self._soup_handler).menu_categories

    def products(self):
        """Returns a list book objects for the current books found on the page"""
        return ProductParser(self._soup_handler, self.url)



# page = BooksToScrapePage("http://books.toscrape.com")
# page.initalize()
