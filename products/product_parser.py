from os.path import join

from web_book_scrapper.products.product_locator import ProductParserLocator
from web_book_scrapper.books.books_parser import BookParser


class ProductParser(object):
    """The class parses all the selector for the products"""
    def __init__(self, soup_handler, site_url):
        self._soup_handler = soup_handler
        self._books_links = None
        self.site_url = site_url

    def get_all_books(self):
        """Returns a list of book objects for the books found on this site. Each book object
           contains the book title, UPC, taxes, price including and excluding tax, etc.
        """
        self._parse_books()

        books = []
        for product in self._books_links:
            book_url = join(self.site_url, product.attrs["href"]).replace("\\", "/")
            books.append(BookParser(self.site_url, book_url))
        return books

    def _parse_books(self):
        """Use the book selector and parses all the books found on the site"""
        self._books_links = self._soup_handler.select(ProductParserLocator.BOOKS_LI) or []

    def __repr__(self):
        return "<Product Parser object>"



