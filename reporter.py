from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

from defs import Bot


class Reporter:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def __del__(self):
        if self.browser is not None:
            self.browser.close()

    def report(self, bot: Bot):
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
