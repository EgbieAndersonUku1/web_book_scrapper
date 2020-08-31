from web_book_scrapper.books import books_element


class BookLocator(object):
    """The class uses the locators to find all the attributes of a given book"""

    BOOKS = books_element.BOOKS
    TITLE = books_element.TITLE
    PRICE = books_element.PRICE
    IMAGE = books_element.IMAGE
    DESCRIPTION = books_element.DESCRIPTION
    RATING = books_element.RATING
    TABLE_ROW_HEADING = books_element.TABLE_ROW_HEADING_TAG
    TABLE_ROW_DATA = books_element.TABLE_ROW_DATA_TAG



