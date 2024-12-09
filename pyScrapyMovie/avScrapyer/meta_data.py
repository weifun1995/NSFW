
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

max_retries = 10

mapping_alias_list = {
    '10musume': {'long': '10musume', 'short': '10mu'},
    '天然むすめ': {'long': '10musume', 'short': '10mu'},
    'pacopacomama': {'long': 'pacopacomama', 'short': 'paco'},
    'パコパコママ': {'long': 'pacopacomama', 'short': 'paco'},
    'caribbeancom': {'long': 'caribbeancom', 'short': 'carib'},
    'カリビアンコム': {'long': 'caribbeancom', 'short': 'carib'},
}

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

series_assert = {
    '人妻マンコ図鑑': {
        'api': 'https://www.pacopacomama.com/dyn/phpauto/movie_details/movie_id/{xxxcarnoxxx}.json',
        'img': 'https://www.pacopacomama.com/moviepages/{xxxcarnoxxx}/images/l_thum.jpg',
        'long_name': 'pacopacomama',
        'short_name': 'paco'
    },
    '秘蔵マンコセレクション': {
        'api': 'https://www.10musume.com/dyn/phpauto/movie_details/movie_id/{xxxcarnoxxx}.json',
        'img': 'https://www.10musume.com/moviepages/{xxxcarnoxxx}/images/l_thum.jpg',
        'long_name': '10musume',
        'short_name': '10mu'
    },
    'マンコ図鑑': { # 阴部图鉴
        'img': 'https://www.caribbeancom.com/moviepages/{xxxcarnoxxx}/images/l_l.jpg',
        'webpage': 'https://www.caribbeancom.com/moviepages/{xxxcarnoxxx}/index.html',
        'series_page': 'https://www.caribbeancom.com/series/989/index.html',
        'long_name': 'caribbeancom',
        'short_name': 'carib'
    },
    'アナル図鑑': { # 屁股图鉴
        'img': 'https://www.caribbeancom.com/moviepages/{xxxcarnoxxx}/images/l_l.jpg',
        'webpage': 'https://www.caribbeancom.com/moviepages/{xxxcarnoxxx}/index.html',
        'series_page': 'https://www.caribbeancom.com/series/1076/index.html',
        'long_name': 'caribbeancom',
        'short_name': 'carib'
},
    'セクシー女優エンサイクロペディア': { # 女优图鉴
        'img': 'https://www.caribbeancom.com/moviepages/{xxxcarnoxxx}/images/l_l.jpg',
        'webpage': 'https://www.caribbeancom.com/moviepages/{xxxcarnoxxx}/index.html',
        'series_page': 'https://www.caribbeancom.com/series/1076/index.html',
        'long_name': 'caribbeancom',
        'short_name': 'carib'
    }
}
