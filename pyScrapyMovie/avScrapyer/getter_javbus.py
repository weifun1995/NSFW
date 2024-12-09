import os
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import urllib.request
import urllib.error
from pathlib import Path
from termcolor import colored
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from pyScrapyMovie.avScrapyer.meta_data import mapping_alias_list

class JavBus:
    def __init__(self, driver, max_retries= 10):
        self.driver = driver
        self.max_retries = max_retries

    def open_page(self, carno):
        print('执行打开页面')
        url = f'https://www.javbus.com/{carno.upper()}'
        webpage = self.get_page_text(url)
        if not webpage:
            print(colored("爬取失败", "red"),  colored(carno, "yellow"))
            return None

        result = self.get_parse_data(webpage)
        return result


    def get_page_text(self, url):

        if not self.driver:
            print('缺少 webdrive')
            return None
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                self.driver.get(url)
                title = self.driver.title
                if '404' in title:
                    print('请求404')
                    return None
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'a.bigImage'))
                )
                page_source = self.driver.page_source
                # if '404 Page Not Found' in page_source:
                #     print('请求404')
                #     return None
                # else:
                return self.driver.page_source
            except Exception as e:
                print()
                print(f"请求出错: {e}。正在进行第 {retry_count + 1} 次重试...")
                retry_count += 1
                time.sleep(2)  # 每次重试前等待2秒，可根据情况调整
        return None


    def get_parse_data(self, webpage):
        soup = BeautifulSoup(webpage, 'html.parser')

        movie_dom = soup.find('div', class_='movie')
        all_a_dom = movie_dom.findAll('a')
        studio = ''
        series = ''
        actor_list = []
        for aaa in all_a_dom:
            if '/studio/' in aaa['href']:
                studio = aaa.text.strip()
            if '/series/' in aaa['href']:
                series = aaa.text.strip()
            if '/star/' in aaa['href']:
                curr_actor_str = aaa.text.strip()
                if curr_actor_str and curr_actor_str not in actor_list:
                    actor_list.append(curr_actor_str)

        print(actor_list)
        actor = '、'.join(actor_list)

        all_p_dom = movie_dom.findAll('p')
        carno = ''
        date = ''
        for ppp in all_p_dom:
            if '識別碼:' in ppp.text:
                carno = ppp.text.replace('識別碼:', '').strip()
            if '發行日期:' in ppp.text:
                date = ppp.text.replace('發行日期:', '').strip()


        thumb_dom = soup.find('a', class_='bigImage')
        print('javbus --- 信息如下')
        thumb = ''
        if thumb_dom:
            thumb = thumb_dom['href']

        titleText = soup.title.text
        print('titleText', titleText)
        title = (titleText.replace('- JavBus', '')
            .replace(carno, '')
            .replace(actor, '')
            .replace('─', '-')
            .replace('−', '-')
            .replace('\u3000', ' ')
            .strip())

        return {
            'release': date,
            'actor': actor,
            'carno': carno,
            'title': title,
            'thumb': 'https://www.javbus.com' +  thumb,
            'website': f'https://www.javbus.com/{carno}',
            'studio': studio,
            'series': series,
            'desc': '',
            'referer': f'https://www.javbus.com/{carno}'
        }