# coding: utf-8

import configparser
import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AutoLiker(object):
    def __init__(self, executable_path='./chromedriver.exe'):
        import instagram_settings as ig

        self.__username = None 
        self.__password = None 
        self.__num_popular_post = 9

        self.__browser = webdriver.Chrome(executable_path=executable_path)

        self.__login_url = ig.login_url
        self.__tag_search_url = ig.tag_search_url

        self.__login_path = ig.login_path
        self.__media_selector = ig.media_selector
        self.__like_selector = ig.like_selector
        self.__next_pager_selector = ig.next_pager_selector

        self.__media_list = None
        self.__media = None
        self.__media_start_num = 0

        self.liked_num = 0

    def load_user_info(self, configfile):
        inifile = configparser.ConfigParser()
        inifile.read(configfile, 'UTF-8')
        self.__username = inifile.get('user', 'name')
        self.__password = inifile.get('user', 'password')

    def login(self):
        self.__browser.get(self.__login_url)
        time.sleep(3)

        self.__browser.find_element_by_xpath(self.__login_path).click()
        time.sleep(3)

        usernameField = self.__browser.find_elements_by_css_selector('form input')[0]
        usernameField.send_keys(self.__username)

        passwordField = self.__browser.find_elements_by_css_selector('form input')[1]
        passwordField.send_keys(self.__password)
        passwordField.send_keys(Keys.RETURN)

    def prepare(self, tagName, avoid_popular_post=False):
        time.sleep(3)
        self.liked_num = 0
        encodedTag = urllib.parse.quote(tagName)
        encodedURL = self.__tag_search_url.format(encodedTag)

        self.__browser.get(encodedURL)
        time.sleep(3)
        self.__browser.implicitly_wait(10)

        self.__media_list = self.__browser.find_elements_by_css_selector(self.__media_selector)

        if avoid_popular_post is True:
            # to avoid popular_post, clicking must start from 9th media.
            self.__media_start_num = self.__num_popular_post
        else:
            self.__media_start_num = 0
        self.__media = self.__media_list[self.__media_start_num]
        self.__media.click()

    def press_like_and_next(self):
        time.sleep(3)
        try:
            self.__browser.find_element_by_css_selector(self.__like_selector).click()
            self.liked_num += 1
            self.__browser.implicitly_wait(10)
            self.__browser.find_element_by_css_selector(self.__next_pager_selector).click()
        except:
            return False
        return True
