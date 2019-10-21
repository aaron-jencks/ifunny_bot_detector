from simple_web import *


homepage = "https://ifunny.co"


class Bot:
    def __init__(self, username: str, url: str, post: list):
        self.user = username
        self.url = url
        self.post = post

    def __eq__(self, other):
        if isinstance(other, Bot):
            return other.user == self.user

    @property
    def user_homepage(self) -> str:
        return homepage + self.url

    @property
    def reasoning_str(self) -> str:
        return ''

    @staticmethod
    def qualifies(user: dict) -> bool:
        profile = simple_get(homepage + user['url'])
        if profile is not None:
            sign = profile.find('div', attrs={'class': 'sign__text'})
            return sign is not None and sign.text == 'no memes yet'
        else:
            print('User {} doesn\'t exist anymore'.format(user['user']))
            return False
