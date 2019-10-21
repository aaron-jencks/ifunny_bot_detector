from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import os
import multiprocessing as mp
from queue import Empty
from tqdm import tqdm

from defs import Bot


def split_arr_evenly(arr: list, num_chunks: int) -> list:
    result = [[] for _ in range(num_chunks)]

    current = 0
    while len(arr) > 0:
        result[current].append(arr.pop(0))

        current += 1

        if current == num_chunks:
            current = 0

    return result


class AsyncReporter(mp.Process):
    def __init__(self, incoming: mp.Queue, stopper: mp.Queue):
        super().__init__()
        self.incoming = incoming
        self.stopper = stopper
        self.reported = []
        self.browser = webdriver.Firefox()

    def report(self, bot: Bot):
        if bot not in self.reported:
            print('Reporting {}'.format(bot.user))
            self.browser.get(bot.user_homepage)
            for b in self.browser.find_elements_by_class_name('profile__control'):
                if 'profile__control_right' not in b.get_attribute('class'):
                    b.click()
                    result = WebDriverWait(self.browser,
                                           10).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                                     'v-dropdown__container')))

                    if result is not None:
                        result = result.find_element_by_class_name('v-list-item')
                        result.click()

                        form = WebDriverWait(self.browser,
                                             10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       'input[name="firstname"]')))

                        if form is not None:
                            form.send_keys('John')

                            form = self.browser.find_element_by_css_selector('input[name="lastname"]')

                            form.send_keys('Smith')

                            form = self.browser.find_element_by_css_selector('textarea[name="address"]')

                            form.send_keys('How about no')

                            form = self.browser.find_element_by_css_selector('input[name="email"]')

                            form.send_keys('iggy12345100@aol.com')

                            form = self.browser.find_element_by_css_selector('input[name="phone"]')

                            form.send_keys('5555555555')

                            form = self.browser.find_element_by_css_selector('textarea[name="details"]')

                            form.send_keys('This is a bot created by Aaron, '
                                           'it\'s sole purpose is to hunt down and report other bots on ifunny, '
                                           'you can find the source code at: '
                                           'https://github.com/iggy12345/ifunny_bot_detector')

                            form = self.browser.find_element_by_css_selector('input[name="relationships"]')
                            form.send_keys('Bot Prosecutor')

                            form = self.browser.find_element_by_css_selector('div.select')
                            form.click()
                            WebDriverWait(self.browser,
                                          10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                    'div.select__container')))
                            form = self.browser.find_elements_by_css_selector('span.select__item')
                            for f in form:
                                if f.find_element_by_css_selector('span.select__item-label').text == "Other":
                                    f.click()
                                    break

                            form = self.browser.find_element_by_css_selector('textarea[name="more"]')
                            form.send_keys(bot.reasoning_str)

                            # time.sleep(1)

                            form = self.browser.find_elements_by_css_selector('button.js-form-submit')
                            for f in form:
                                f.click()
                                f.submit()

                            time.sleep(4)

                            self.reported.append(bot)
                        else:
                            print('Opening selection dropdown failed')
                    else:
                        print('Loading the user\'s profile failed')
        else:
            print('The user {} has already been reported'.format(bot.user))

    def run(self) -> None:
        while True:
            if not self.incoming.empty():
                self.report(self.incoming.get())

            if not self.stopper.empty():
                print('Stopping browser')
                self.incoming.close()
                self.stopper.close()
                self.browser.close()
                return None


class Reporter:

    num_instances = os.cpu_count()

    def __init__(self):
        self.reporters = []
        self.rqs = []
        self.stoppers = []
        self.current_q = 0

        print('Generating Firefox instances')
        for _ in tqdm(range(self.num_instances)):
            iq = mp.Queue()
            sq = mp.Queue()
            rep = AsyncReporter(iq, sq)
            self.rqs.append(iq)
            self.stoppers.append(sq)
            self.reporters.append(rep)
            rep.start()

    def __del__(self):
        for s in self.stoppers:
            s.put(True)

    def report(self, bot: Bot):
        self.rqs[self.current_q].put(bot)
        self.current_q += 1

        if self.current_q == self.num_instances:
            self.current_q = 0

    def report_multiple(self, bots: list):
        for b in bots:
            self.report(b)

