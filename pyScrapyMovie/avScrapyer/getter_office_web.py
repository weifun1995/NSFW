import requests
from termcolor import cprint
from pyScrapyMovie.avScrapyer.meta_utils import get_api_json, parse_json, get_page_data, get_carib_details
from bs4 import BeautifulSoup


maker_assert = {
    'kin8': {
        'function': 'maker_kin8'
    },
    'lesshin': {
        'function': 'maker_lesshin_nyoshin',
        'args': ['lesshin']
    },
    'nyoshin': {
        'function': 'maker_lesshin_nyoshin',
        'args': ['nyoshin']
    },
    'carib': {
        'function': 'maker_carib'
    },
    '10mu': {
        'function': 'maker_json',
        'args': ['10musume']
    },
    'paco': {
        'function': 'maker_json',
        'args': ['pacopacomama']
    },
}
def maker_page( webpage):
    webpage = get_page_data(webpage)
    if not webpage:
        cprint(f'-> x 查询到官网信息失败')
    return get_carib_details(webpage)

class MakerScrapyer:
    def __init__(self, filename):
        self.series = ''
        self.args = ''
        self.filename = filename.lower()
        self.carno = self.get_carno()

    def init(self):
        print('匹配到：', self.filename, self.carno, self.series )
        if not self.series:
            return None
        # 根据规范命名获取 车牌号
        if not hasattr(self, self.series):
            print('没有实现函数')
            return '没有实现函数'
        print('官网处理', self.series, self.args, self.carno)
        function_to_call = getattr(self, self.series)
        if not function_to_call:
            cprint('-> 不能匹配到需要处理的series函数 ')

        if self.args:
            movie_info = function_to_call(self.carno, *self.args)
        else:
            movie_info = function_to_call(self.carno)
        return movie_info

    def get_carno(self):
        carno = self.filename
        for maker_item in maker_assert.keys():
            if maker_item in self.filename:
                self.series = maker_assert[maker_item]['function']
                if 'args' in maker_assert[maker_item]:
                    self.args = maker_assert[maker_item]['args']
                arr = self.filename.split('-')
                if len(arr) > 1:
                    carno = '-'.join(arr[1:])
                else:
                    print(f'文件命名错误，终端爬取操作：{self.filename}')
                break
        return carno

    def maker_kin8(self, carno):
        url = f'https://en.kin8tengoku.com/moviepages/{carno}/index.html'
        page_souce = get_page_data(url)
        if not page_souce:
            return None
        soup = BeautifulSoup(page_souce, 'html.parser')
        thumb = f'https://en.kin8tengoku.com/{carno}/pht/main_en.jpg'

        detail_dom = soup.findAll('td', class_='movie_table_td2')

        release = detail_dom[-1].text.strip()

        actorList = []
        actor_dom = detail_dom[0].findAll('a')
        for item_actor in actor_dom:
            actorList.append(item_actor.text.strip())

        carid = f'kin8tengoku.{carno}'
        title = soup.title.text.strip().split('Kin8tengoku.com')[0].strip()

        actor = '、'.join(actorList)
        # 去掉title的人名
        if f'({actor})' in title:
            title = title.replace(f'({actor})', '')
        if actor in title:
            title = title.replace(actor, '')

        deta = release.replace('-','.')
        filename =  f'kin8tengoku-{carno}({deta}){title}({actor})'
        obj = {
            'id': carid,
            'carno': carno,
            'release': release,
            'title': title,
            'actor': actor,
            'desc': title,
            'thumb': thumb,
            'filename': filename
        }
        return obj

    def maker_lesshin_nyoshin( self, carno, series):
        carno = carno.lower()
        if 'n' in carno:
            carno = carno.split('n')[1:]

        url = f'https://www.{series}.com/moviepages/n{carno}/index.html'

        page_souce = get_page_data(url)
        if not page_souce:
            return None
        soup = BeautifulSoup(page_souce, 'html.parser')

        title = soup.title.text.strip()

        info = soup.find('div', id="information")

        table = info.findAll('td', class_="table_right")

        release = table[0].text.strip()

        actor_list = []
        actor_dom = table[1].findAll('a')
        for item in actor_dom:
            actor_list.append(item.text.strip())
        actor = '、'.join(actor_list)

        timer = release.replace('-', '.')

        carid = f'{series}.{timer}.n{carno}'

        desc = info.find('div', id="info_comment").text.strip()

        post = f'/moviepages/n{carno}/index.html'

        thumb = f'https://www.lesshin.com/contents/{carno}/thum2.jpg'

        temp_arr  = title.split('|')
        subTitle = ''
        if len(temp_arr) > 1:
            subTitle = temp_arr[1].strip()

        filename = f'{series}.n{carno}({timer}){subTitle}({actor})'

        obj = {
            'id': carid,
            'carno': carno,
            'release': release,
            'title': title,
            'actor': actor,
            'series': series,
            'desc': desc,
            'thumb': thumb,
            'website': post,
            'filename': filename
        }
        return obj

    def maker_carib(self, carno):
        url = f'https://www.caribbeancom.com/moviepages/{carno}/index.html'
        print('爬取 carib', url)

        page_souce = get_page_data(url)
        if not page_souce:
            return None
        soup = BeautifulSoup(page_souce, 'html.parser')

        title = soup.find('div', class_="heading").find('h1').text.strip()

        desc = soup.find("p", itemprop="description").text.strip()

        actorList = soup.find('span', class_='spec-content').findAll('span', itemprop="name")

        releaseDom = soup.find('span', itemprop="datePublished")
        release = ''
        if releaseDom:
            release = releaseDom.text.strip().replace('/', '-')

        if not release and carno:
            release = '20' + carno[4:6] + '-' + carno[0:2] + '-' + carno[2:4]

        seriesDom = soup.title
        series = ''
        if seriesDom:
            series = seriesDom.text.strip().split(' ')[0]

        postDom = soup.find('link', hreflang="en-US")
        post = ''
        if postDom:
            post = postDom['href'].split('eng')[1]

        timer = release.replace('-', '.')

        carid = f'caribbeancom.{release}.{carno}'

        thumb = f"https://www.caribbeancom.com/moviepages/{carno}/images/l_l.jpg"

        name_list = []
        for name in actorList:
            namestr = name.text.strip()
            if namestr and namestr not in name_list:
                name_list.append(namestr)

        actor = '、'.join(name_list)

        filename = f'caribbeancom.{timer}({carno}){title}({actor})'

        obj = {
            'id': carid,
            'carno': carno,
            'title': title,
            'actor': actor,
            'release': release,
            'desc': desc,
            'thumb': thumb,
            'website': url,
            'filename': filename,
            'type': '',
            'tags': '',
            'maker': 'caribbeancom.com',
            'series': series,
        }
        return obj

    def maker_json(self, carno, studio):
        weburl = f'https://www.{studio}.com/dyn/phpauto/movie_details/movie_id/{carno}.json'
        json = get_api_json(weburl)
        if not json:
            return None
        thumb = json['ThumbHigh']
        title = json['Title']
        actor = json['Actor'].replace(',', '、')
        carno = json['MovieID']
        series = json['Series']
        release = json['Release']
        timer = release.replace('-', '.')
        desc = json['Desc'].replace('\r', '').replace('\n', '').replace('<br>', '')
        type = ''
        tags = ''

        # if not series:
        #     series = '秘蔵マンコセレクション'
        if series and series in title:
            filename = f'{studio}.{timer}({carno}){title}({actor})'
        else:
            if series:
                filename = f'{studio}.{series}.{timer}({carno}){title}({actor})'
            else:
                filename = f'{studio}.{timer}({carno}){title}({actor})'

        if '秘蔵マンコセレクション' in title:
            title = f'秘蔵マンコセレクション_{release}_{actor}'
            filename = f'{studio}.{timer}({carno})秘蔵マンコセレクション({actor})'
            type = '図鑑'
            tags = '図鑑、女体、阴道、屄、puss'

        return {
            'id': f'{studio}.{timer}.{carno}',
            'carno': carno,
            'title': title,
            'actor': actor,
            'release': release,
            'desc': desc,
            'thumb': thumb,
            'website':f'https://www.{studio}.com/movies/{carno}/',
            'filename': filename,
            'type': type,
            'tags': tags,
            'maker': f'{studio}.com',
            'series': series,
        }
