from tqdm import tqdm
import multiprocessing as mp
import os

from simple_web import *
from defs import homepage
import bot_defs as bd


def is_bot(comment_dict: dict) -> bd.Bot:
    for b in bd.bot_list:
        if b.qualifies(comment_dict):
            return b(comment_dict['user'], comment_dict['url'], comment_dict['text'])

    return None


class IFunnyServer:
    def __init__(self):
        self.page = 1
        self.page_data = None
        self.comment_urls = []
        self.comments = []
        self.pool = mp.Pool(os.cpu_count())

    def __del__(self):
        self.pool.close()

    def get_page(self) -> bool:
        self.page_data = simple_get(homepage + "/page{}".format(self.page))
        return self.page_data is not None

    def next_page(self) -> bool:
        self.page += 1

        if not self.get_page():
            self.page -= 1
            self.get_page()
            return False

        return True

    def prev_page(self):
        self.page -= 1

        if self.page == 0:
            self.page = 1
            return False

        if not self.get_page():
            self.page += 1
            self.get_page()
            return False

        return True

    def find_comment_urls(self) -> list:
        if self.page_data is not None or self.get_page():

            bs4_posts = self.page_data.find_all("div", class_="post")

            self.comment_urls = []

            for p in bs4_posts:
                self.comment_urls.append(homepage +
                                         str(p.find_all("a",
                                                        class_="post-actions__link",
                                                        attrs={"data-goal-id": "feed_post_comments"})[0]['href']))

            return self.comment_urls

        return []

    @staticmethod
    def find_comment(url: str) -> list:
        comment_section = simple_get(url)
        dicts = []
        if comment_section is not None:
            comment_objs = comment_section.find_all("div", class_="comment")
            for co in comment_objs:
                user = co.find_all("a", attrs={'data-goal-id': 'post_commentauthor'})

                if len(user) < 2:
                    continue
                else:
                    user = user[1]

                texts = co.find_all("span", class_="comment__message")
                user_dict = {'user': user.text,
                             'url': user['href'],
                             'text': []}
                for t in texts:
                    user_dict['text'].append(t.text)

                dicts.append(user_dict)
        return dicts
    
    def find_comments(self) -> list:
        if len(self.comment_urls) == 0:
            self.find_comment_urls()

        self.comments = []
        for l in self.pool.imap(self.find_comment, self.comment_urls):
            self.comments += l

        return self.comments

    def detect_bots(self) -> list:
        bots = []

        for b in self.pool.imap(is_bot, self.comments):
            if b is not None:
                bots.append(b)

        # for c in tqdm(self.comments):
        #     b = is_bot(c)
        #     if b is not None:
        #         bots.append(b)

        return bots

    def find_everything(self) -> list:
        self.page = 1
        self.get_page()

        everything = []
        bots = []

        first = True
        while first or self.next_page():
            if first:
                first = False

            print('Collecting page {}'.format(self.page))
            everything += self.find_comments()
            bots += self.detect_bots()

        return everything
