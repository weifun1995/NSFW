import json
import re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from pyScrapyMovie.avScrapyer import meta_utils
from pyScrapyMovie.aTools import utils





class Got2Pee:
    def __init__(self, dir_folder):
        self.folder = dir_folder
        pass

    def format_date(self, date_str):
        """
        将指定格式的日期字符串（如'Nov 22, 2024'）转换为'2024-11-22'格式。
        参数:
        date_str (str): 需要转换格式的日期字符串，格式需类似'Nov 22, 2024'
        返回:
        str: 转换后的日期字符串，格式为'2024-11-22'
        """
        try:
            # 使用strptime方法将输入的日期字符串解析为datetime对象
            date_obj = datetime.strptime(date_str, '%b %d, %Y')
            # 使用strftime方法将datetime对象格式化为指定的输出格式
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            print(f"输入的日期字符串 {date_str} 格式不符合要求，请检查格式是否类似 'Nov 22, 2024'")
            return None

    # 由于有些文件名 不是key值对应的详情页码 需要根据标题去匹配
    def get_pagelist_data(self, start_no, end_no):
        arr = []
        for pageno in range(int(start_no), int(end_no) + 1):
            url = f'https://got2pee.com/videos/page-{pageno}/?tag=all&sort=recent'
            print('当前分页：' , url)
            webpage = meta_utils.get_page_data(url)
            # print(webpage)
            if  webpage:
                temp_res = self.parse_webpage('page', webpage)
                if temp_res:
                    arr += temp_res

        print('data', arr)
        txt_path = self.folder / '分页数据.json'
        with open(txt_path, 'w', encoding='utf-8') as file:
            json.dump(arr, file)

    def get_detail_data(self, key):
        url = f'https://got2pee.com/videos/{key}/'
        webpage = meta_utils.get_page_data(url)
        if not webpage:
            res = self.parse_webpage('detail', webpage)
            return res

    def parse_webpage(self, tag='page', webpage=''):
        print('222')
        soup = BeautifulSoup(webpage, 'html.parser')
        obj = {
            'maker': 'got2pee.com',
            'series': '',
            'type': 'pee',
            'tag': 'pee、outdoor、小便、尿尿、户外',
            'actor': ''
        }
        # 列表页
        if tag == 'page':
            arr = []
            try:
                video_frame_list = soup.findAll('div', class_='video-frame')
                if len(video_frame_list) < 1:
                    return None

                for video in video_frame_list:
                    item_obj = obj
                    img_box = video.find('img')
                    if img_box:
                        item_obj['thumb'] = img_box['src']

                    website_box = video.find('a')
                    if website_box:
                        item_obj['website'] = website_box['href']
                        item_obj['key'] = website_box['href'].split('/')[-2]

                    title_box = video.find('span', class_='name')
                    if title_box:
                        item_obj['key'] = title_box.text.strip()

                    release_box = video.find('span', class_='left')
                    if release_box:
                        release = release_box.text.strip()
                        item_obj['release'] = self.format_date(release)

                    print('当前 item_obj', item_obj)

                    arr.append(item_obj)
                return arr
            except AttributeError:
                print("未找到video - frame标签")
                return None
        else:
            # 详情页
            video_frame = soup.findAll('div', class_='video-envelope')

            meta_tag = soup.find('meta', attrs={'name': 'expires'})
            if meta_tag:
                content_value = meta_tag.get('content')
                try:
                    # 解析原始日期时间字符串为datetime对象
                    date_obj = datetime.strptime(content_value, '%a, %d %b %Y %H:%M:%S %z')
                    # 将datetime对象格式化为指定的输出格式
                    obj['release'] = date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    print(f"日期时间格式不符合要求，原始内容为 {content_value}")

            img_box = video_frame.find('img')
            if img_box:
                obj['thumb'] = img_box['src']
                key = img_box['src'].split('/')[-3]
                obj['key'] = key
                obj['website'] = f'https://got2pee.com/videos/{key}/'

            desc_box = soup.find('div', class_='movie-description')
            if desc_box:
                text = desc_box.text
                match = re.search(r'About video:(.*)\n', text)
                if match:
                    obj['desc'] = match.group(1)

            obj['doc_title'] = soup.title
            return obj




if __name__ == '__main__':
    dir = Path(r'E:\avplace\【Pee】Got2Pee\Got2Pee 2023.07.18-2024.03.25\Video')
    page_list_txt = dir / '分页数据.json'
    detail_list_txt = dir / '详情数据.json'

    got2pee = Got2Pee(dir)
    # got2pee.get_pagelist_data(10,10 )
    # got2pee.get_pagelist_data(10,23 )

    print(111, got2pee.format_date('Nov 22, 2024'))
    pass