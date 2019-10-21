import re

from defs import *


class SupportBot(Bot):
    regex = re.compile(r'Support[0-9_]+')

    @staticmethod
    def qualifies(user: dict) -> bool:
        return SupportBot.regex.match(user['user']) is not None and Bot.qualifies(user)

    @property
    def reasoning_str(self) -> str:
        return 'The user {} has been caught spamming comment sections trying to gain attention ' \
               'for an offensive and fake website by impersonating ifunny personnel.'.format(self.user)


class TityKissBot(Bot):
    regex = re.compile(r'titykiss')

    @staticmethod
    def qualifies(user: dict) -> bool:
        return 'titykiss' in str(user['text']) is not None and Bot.qualifies(user)

    @property
    def reasoning_str(self) -> str:
        return 'The user {} is baiting comment sections for a fake snapchat account used for scamming ' \
               '(it\'s a porn bot)'.format(self.user)


bot_list = [SupportBot, TityKissBot]
