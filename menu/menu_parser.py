from bs4 import BeautifulSoup

from web_book_scrapper.menu.menu_locator import MenuLocator


class MenuParser(object):
    def __init__(self, soup_handler):
        self._soup = soup_handler

    @property
    def menu_categories(self):
        """Return all the categories found on the page"""
        categories_list = self._soup.select(MenuLocator.MENU_CATEGORIES)
        return [category.string.strip() for category in categories_list if category]

