from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    try:
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)
    except KeyError:
        print('Website response was empty')
        return False


def simple_get(url: str):
    """Retrieves the contents of a given url"""

    try:
        attempt = 0
        while attempt < 5:
            with closing(get(url, stream=True)) as resp:
                if is_good_response(resp):
                    return BeautifulSoup(resp.content, 'html.parser')
                else:
                    attempt += 1
        print('Failed to get a good response within 5 attempts')
        return None
    except RequestException as e:
        print("Something went wrong while trying to get the webpage!")
        return None
