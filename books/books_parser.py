from os.path import join

import requests

from bs4 import BeautifulSoup

from web_book_scrapper.books.books_locator import BookLocator
from web_book_scrapper.utils.search import match_search


class BookParser(object):
    def __init__(self, url, book_url):
        self.url = url
        self.book_url = book_url
        self._soup_handler = None
        self._row_elements = []
        self._table_data = {}
        self._initalize_ckass = False

    def __repr__(self):
        if not self._initalize_ckass:
            return f"BookParser: <url: {self.url}>"
        return f"<BookParser obj: title: <{self.title.title()}>"

    def initialize(self):
        """Initialize the BookParser object must be run first before the methods are used otherwise
           a none value will be returned.
        """
        page = requests.get(self.book_url)
        self._soup_handler = BeautifulSoup(page.content, "html.parser")
        self._extract_table_content()
        self._initalize_ckass = True

    def _extract_table_content(self):
        """Extract the table content from the page of the website"""
        row_headings_list = self._soup_handler.find_all(BookLocator.TABLE_ROW_HEADING)
        row_data_list = self._soup_handler.find_all(BookLocator.TABLE_ROW_DATA)
        self._create_table_content_dictionary(row_headings_list, row_data_list)

    def _create_table_content_dictionary(self, row_headings_list, row_data_list):
        """_create_table_content_dictionary(list, list) -> return None

          Takes two list. The first one contains a list of row of headings. The second
          list contains the data associated with that heading. It takes the two lists
          and turns in to a dictionary with heading as the key and data associated with
          it as the value.

          e.g
          list = [heading, heading2..........heading_n]
          list2 = [data_associated_with heading1, data_associated_with_heading2.........data_associated_with_heading_n]

        """
        self._table_data = {row_headings_list[idx].string:row_data_list[idx].string for idx in range(len(row_headings_list)) }

    @property
    def title(self):
        """returns the title of the book"""
        return self._if_object_is_true_return_string(self._soup_handler.select_one(BookLocator.TITLE))

    @property
    def price(self):
        """returns the price of the book"""
        return self._string_to_float(self._if_object_is_true_return_string(self._soup_handler.select_one(BookLocator.PRICE)))

    @property
    def description(self):
        """returns the description of the book"""
        return self._if_object_is_true_return_string(self._soup_handler.select_one(BookLocator.DESCRIPTION))

    @property
    def rating(self):
        """Return the rating of the book"""
        ratings = self._soup_handler.select_one(BookLocator.RATING)
        if len(ratings) > 1:
            return [classes for classes in ratings.attrs["class"] if classes != "star-rating"][0]

    @property
    def image_link(self):
        """Return the image link for the book"""
        img_tag = self._soup_handler.select_one(BookLocator.IMAGE)
        if img_tag:
            return join(self.url, img_tag.attrs["src"].split("../")[2]).replace("\\", "/")

    @property
    def upc(self):
        """Return the UPC of the book"""
        return self._table_data.get("UPC")

    @property
    def product_type(self):
        """Returns the type item the product is"""
        return self._table_data.get("Product Type")

    @property
    def price_including_tax(self):
        """Returns the price of the item including the tax"""
        return self._string_to_float(self._table_data.get("Price (incl. tax)"))

    @property
    def price_excluding_tax(self):
        """Returns the price of the book excluding the tax"""
        return self._string_to_float(self._table_data.get("Price (excl. tax)"))

    @property
    def availabilty(self):
        """Returns the availability of the book along with the current stock"""
        return self._table_data.get("Availabilty")

    @property
    def tax(self):
        """Returns the amount of tax charged to the item"""
        return self._table_data.get("Tax")

    @property
    def num_of_reviews(self):
        """Returns the number of reviews for the book"""
        return self._table_data.get("Number of reviews")

    def _if_object_is_true_return_string(self, value):
        """_if_value_is_true_then(beautifulSoup obj) -> returns None or string

          Takes a beautifulSoup object and returns the string associated with
          that object. If the object is None returns a None value.
        """
        return value.string if value else None

    def _if_list_not_empty_parse(self, position_number):
        """_if_list_not_empty_parser(int) -> return empty list
          Takes a number for a list containing a row of tag objects and returns
          the string value associated with that position for the list.
        """
        return self._row_elements[position_number].string if self._row_elements else []

    def _string_to_float(self, string):
        """_string_to_float(str) -> return int
           Takes a given string and turns that string into a float
        """
        if string:
            pattern = "£([0-9]+\.[0-9]+)"
            match = match_search(pattern, string)
            return float(match.group(1)) if match else None

