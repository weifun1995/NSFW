import os
import requests
import re
from termcolor import cprint
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from selenium import webdriver
from termcolor import colored
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

from pyScrapyMovie.avScrapyer.meta_data import headers, max_retries

def get_api_json(url, retries=10):
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, verify=False)
            cprint(f'-> 状态码: {response.status_code}')
            if response.status_code == 404:
                cprint(f"-> 请求出错：404", 'yellow')
                return None
            if response.status_code == 200:
                return response.json()
            response.raise_for_status()
        except RequestException as e:
            cprint(f"请求出错: {e}, 正在重试...", 'yellow')
    cprint(f"经过 {retries} 次重试后仍无法获取数据", 'red')
    return None


def parse_json(series, json):
    obj = {
        'poster': json['MovieThumb'],
        'title': json['Title'],
        'actor': json['Actor'].replace(',', '、'),
        'carno': json['MovieID'],
        'series': json['Series'],
        'date': json['Release'].replace('-', '.')
    }
    filename = obj['series'] + '.' + obj['date'] + '_番号：' + obj['carno'] + '女优：' + obj['actor']
    if obj['series'] == '人妻マンコ図鑑':
        num = obj['title'].replace(obj['series'], '').strip().split(' ')[0].strip()
        filename = f'n{num}_{filename}'
    obj['filename'] = filename
    return obj


# 请求网页
def get_page_data(url, retries=10):
    for _ in range(retries):
        try:
            response = requests.get(url, headers=headers, verify=False)
            print(response.status_code)
            print(response.history)
            if response.history:
                # 获取原始请求状态码
                if response.history[0].status_code != 200:
                    print('网页进行了重定向，应该是没有找到数据')
                    return None

            if response.status_code == 200:
                # 检测页面的编码
                pcharset = 'UTF-8'
                match = re.search(r'<meta http-equiv="Content-Type" content="text/html; charset=(.*)">', response.text)
                if match:
                    charset = match.group(1)
                    pcharset = charset
                    cprint(f'-> 爬取到编码: {charset}', 'blue')
                else:
                    cprint(f'-> 未找到编码信息', 'red')

                page_content = response.content
                try:
                    page_content = response.content.decode(pcharset).encode('utf-8')
                except:
                    cprint(f'-> 尝试编码解析失败{pcharset} - UTF-8', 'red')
                return page_content
            else:
                return None
            # response.raise_for_status()
        except RequestException as e:
            cprint(f"-> 请求出错: {e}, 正在重试...", 'yellow')

    cprint(f"-> 经过 {retries} 次重试后仍无法获取数据", 'red')
    return None


def get_carib_details(content):
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.find('div', class_="heading").find('h1').text.strip()

    actorList = soup.find('span', class_='spec-content').findAll('span', itemprop="name")

    releaseDom = soup.find('span', itemprop="datePublished")
    release = ''
    website = 'https://www.caribbeancom.com'
    if releaseDom:
        release = releaseDom.text.strip().replace('/', '.')

    name_list = []
    for name in actorList:
        name_list.append(name.text.strip())

    actor = '、'.join(name_list)
    return (title, release, actor)


# 下载图片
def down_image(image_url, local_path, referer_url=''):
    cprint(f'---> 图片地址{image_url}', 'blue')
    max_retries = 10
    for retry_count in range(max_retries):
        headers = {
            "Referer": referer_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(image_url, headers=headers)
        cprint(f'---> 下载图片的状态码：{response.status_code}', 'yellow')
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            cprint(f'---> 海报下载成功', 'green')
            return True
        else:
            retry_count += 1
            cprint(f"---> HTTP错误: {response.status_code}，正在进行第 {retry_count + 1} 次重试，等待3秒...", 'red')
    cprint(f'---> 达到最大重试次数，文件下载失败', 'red')
    return False


class EdgeDrive:
    def __init__(self):
        self.driver = None

    def open(self):
        print('开始 selenium 爬取')
        edge_options = webdriver.EdgeOptions()

        # edge_options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images": 2}
        edge_options.add_experimental_option("prefs", prefs)
        # 启用优化设置，这将阻止图片加载
        # edge_options.add_experimental_option('useAutomationExtension', False)

        driver = webdriver.Edge(options=edge_options)
        # 设置网页不加载图片
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "deny",
            "download_path": ""
        })

        self.driver = driver
        return driver

    def close(self):
        if self.driver:
            self.driver.close()
        else:
            print('没有初始化edge drive')

class ChromeDrive:
    def __init__(self):
        self.driver = None

    def open(self):
        print('开始 selenium 爬取')
        chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

        # 使用本地下载的 游览器
        exe_path = 'chromedriver-win64-131.0.6778.85/chromedriver.exe'
        current_file_abs_path = os.path.abspath(__file__)
        current_dir_abs_path = os.path.dirname(current_file_abs_path)
        absolute_path_exe = os.path.abspath(os.path.join(current_dir_abs_path, exe_path))
        print(f'chrome 位置 {absolute_path_exe}',  os.path.exists(absolute_path_exe))
        # chrome_options.binary_location = absolute_path_exe

        service = Service(absolute_path_exe)
        driver = webdriver.Chrome(service = service,options=chrome_options)
        # 设置网页不加载图片
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "deny",
            "download_path": ""
        })

        self.driver = driver
        return driver

    def close(self):
        if self.driver:
            self.driver.close()
        else:
            print('没有初始化edge drive')

def format_movie_info(movie_obj):
    mapping_alias_list = {
        '10musume': {'long': '10musume', 'short': '10mu'},
        '天然むすめ': {'long': '10musume', 'short': '10mu'},
        'pacopacomama': {'long': 'pacopacomama', 'short': 'paco'},
        'パコパコママ': {'long': 'pacopacomama', 'short': 'paco'},
        'caribbeancom': {'long': 'caribbeancom', 'short': 'carib'},
        'カリビアンコム': {'long': 'caribbeancom', 'short': 'carib'},
    }
    carib_list = ['マンコ図鑑', 'アナル図鑑', '女優エンサイクロペディア']

    def get_obj_data(obj, key, default=''):
        if key in obj.keys():
            return obj[key]
        return default
    def remove_invalid_chars(filename):
        invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename
    def has_carib(title):
        for item in carib_list:
            if item in title:
                return item
        return False

    def get_studio():
        temp_series = get_obj_data(movie_obj, 'series')
        if temp_series :
            for item in mapping_alias_list.keys():
                if temp_series == item:
                    return mapping_alias_list[item]['short']
        return ''

    movie_obj['studio'] = get_studio()

    # obj = movie_obj
    obj = {}
    timer = get_obj_data(movie_obj, 'release').replace('-', '.')
    carno = get_obj_data(movie_obj, 'carno')
    release =  get_obj_data(movie_obj, 'release')
    actor = get_obj_data(movie_obj, 'actor')

    if '秘蔵マンコセレクション' in movie_obj['title']:
        obj['type'] = '図鑑'
        obj['tags'] =' 図鑑、女体、阴道、屄、pussy'
        obj['maker'] = '10musume.com'
        obj['series'] = '秘蔵マンコセレクション'
        obj['studio'] = '10mu'
    elif '人妻マンコ図鑑' in movie_obj['title']:
        obj['type'] = '図鑑'
        obj['tags'] = ' 図鑑、女体、阴道、屄、人妻、pussy'
        obj['maker'] = 'pacopacomama.com'
        obj['series'] = '人妻マンコ図鑑'
        obj['studio'] = 'paco'
        obj['title'] = f"{movie_obj['title']}_{release}_{actor}"
        obj['filename'] = f'pacopacomama.{timer}({movie_obj["carno"]}){movie_obj["title"]}({movie_obj["actor"]})'
    elif has_carib(movie_obj['title']):
        obj['type'] = '図鑑'
        obj['tags'] = ' 図鑑、女体、阴道、屄、pussy'
        obj['maker'] = 'caribbeancom.com'
        obj['series'] = has_carib(movie_obj['title'])
        if has_carib(movie_obj['title']) == 'アナル図鑑':
            obj['tags'] = ' 図鑑、女体、屁股、尻、ass'
        obj['studio'] = 'carib'
    else:
        obj['filename'] =  movie_obj['filename']
        pass

    # 对 描述 进行删除一些字符
    if get_obj_data(movie_obj, 'desc'):
        arr = ['\r', '\n', '<br>']
        str = get_obj_data(movie_obj, 'desc')
        for item in arr:
            str = str.replace(item, '')
        obj['desc'] = str


    title = movie_obj['title']
    maker = obj['maker']
    series = obj['series']
    if obj['series']:
        obj['title'] = get_obj_data(obj, 'title') if get_obj_data(obj, 'title') else f'{series}_{release}_{actor}'
    else:
        obj['title'] = get_obj_data(obj, 'title') if get_obj_data(obj, 'title') else  f'{movie_obj["title"]}_{release}_{actor}'

    host = obj['maker'].replace('.com', '')

    temp_filename = get_obj_data(obj, 'filename') if get_obj_data(obj, 'filename') else  f'{host}.{timer}({movie_obj["carno"]}){obj["series"]}({movie_obj["actor"]})'

    obj['filename'] = remove_invalid_chars(temp_filename)

    obj['id'] = f'{host}.{timer}.{movie_obj["carno"]}'
    movie_obj.update(obj)
    return movie_obj
