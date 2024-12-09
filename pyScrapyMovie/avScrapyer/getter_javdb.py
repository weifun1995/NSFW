import requests
from pyScrapyMovie.avScrapyer.meta_data import headers, max_retries, mapping_alias_list,series_assert
from termcolor import cprint
from bs4 import BeautifulSoup
from pyScrapyMovie.avScrapyer.meta_utils import get_page_data

class JavDB:
    def __init__(self, carno):
        self.carno = carno
        self.info = {}
        self.info['carno'] = carno

    def init(self):
        card_soup = self.javdb_search()
        if not card_soup:
            return None

        obj1 = self.javdb_card(card_soup)
        if not obj1:
            return None

        self.info.update(obj1)

        obj2 = self.javdb_detail()
        self.info.update(obj2)

        studio = self.info['studio']
        studioStr = ''
        if studio and studio in mapping_alias_list :
           studio = mapping_alias_list[studio]['long']
           studioStr = f'{studio}.'

        date = self.info['date']
        carno = self.info['carno']
        titleText = self.info['title']
        title = (titleText
            .replace(carno, '')
            .replace('─', '-')
            .replace('−', '-')
            .replace('\u3000', ' ')
            .replace(':', ' ')
            .strip())

        actor = self.info['actor']
        self.info['filename'] = f'{studioStr}{date}({carno}){title}({actor})'

        return self.info

    # 搜索影片
    def javdb_search(self):
        webpage_url = f'https://javdb.com/search?q={self.carno}'
        cprint(f'-> 开始javDB爬取：{webpage_url} ', 'yellow')
        retry_count = 0
        while retry_count < max_retries:
            try:
                req = requests.get(url=webpage_url, headers=headers)
                if req.status_code == 200:
                    cprint('-> √ 爬取成功', 'green')
                    return req.text
                else:
                    retry_count += 1
                    cprint(f'-> x 状态码: {req.status_code}, 进行第 {retry_count} 次重试 ', 'yellow')
            except Exception as e:
                cprint(f'-> x 出现错误:推断代理问题 {e}', 'red')
                return None
        cprint('-> x 经过 10 次重试仍然失败', 'red')
        return None

    # 找到影片的card
    def javdb_card(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        dom_404 = soup.find('div', class_="empty-message")
        if dom_404:
            cprint('-> 没有找到相关的影片信息', 'red')
            return None

        dom_movies = soup.find('div', class_="movie-list").find_all('div', class_='item')

        carno_card = ''
        for item in dom_movies:
            car_num = item.find('strong').text.strip()
            if car_num == self.carno:
                cprint('-> 找到了影片', 'green')
                carno_card = item
                break

        if not carno_card:
            cprint('-> 没有找到匹配的车号信息', 'red')
            return None

        title = carno_card.find('a')['title'].strip()
        cprint(f'--> 标题：{title}', 'blue')

        link = 'https://javdb.com' + carno_card.find('a')['href'].strip()
        cprint(f'--> 详情链接：{link}', 'blue')

        date = carno_card.find('div', class_='meta').text.strip().replace('-', '.')
        cprint(f'--> 发行时间：{date}', 'blue')

        thumb = carno_card.find('img')['src']
        cprint(f'--> 封面：{thumb}', 'blue')

        return {
            'title': title,
            'link': link,
            'date': date,
            'thumb': thumb
        }


    def javdb_detail(self):
         detail_link = self.info['link']
         content = get_page_data(detail_link)
         soup = BeautifulSoup(content, 'html.parser')
         movie_dom = soup.find('div', class_='video-detail')
         info_item = soup.findAll('div', class_="panel-block")
         actor_list = []
         studio = ''
         series = ''
         for item in info_item:
             strong_dom = item.find('strong')
             if not strong_dom:
                 continue
             subTitle = strong_dom.text.strip()
             if subTitle == '片商:':
                 maker_dom = item.find('a')
                 if maker_dom:
                     studio = maker_dom.text.strip()
             if subTitle == '系列:':
                 series_dom = item.find('a')
                 if series_dom:
                     series = series_dom.text.strip()
             if subTitle == '演員:':
                 actor_dom = item.findAll('a')
                 for bb in actor_dom:
                     temp_actor = bb.text.strip()
                     if temp_actor and temp_actor not in actor_list:
                         actor_list.append(temp_actor)

         actor = '、'.join(actor_list)
         if not studio:
             for item in series_assert.keys():
                 if item in self.info['title']:
                     studio = series_assert[item]['long_name']
                     thumb =  series_assert[item]['img']
         obj = {
             'actor': actor,
             'studio': studio,
             'series': series
         }
         if thumb:
            obj['thumb'] = thumb.replace('{xxxcarnoxxx', self.carno)
         return obj
