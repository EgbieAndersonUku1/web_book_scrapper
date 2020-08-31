from re import search


def match_search(pattern, string):
    """match_search(str, str) -> returns a group object

       Takes two parameters that are both strings.
       The first element is the pattern that will be used to match
       against a given string. The second element is the string
       that will be matched. If the string is matched the function
       returns a group or object containing the given matched string
       otherwise returns None
    """
    return search(pattern, string)