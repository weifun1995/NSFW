import codecs
import os
import re
from pathlib import Path
import xml.etree.ElementTree as ET
import json
import configparser
import requests
from termcolor import cprint
from pyScrapyMovie.aTools import mysqlite3
class MyOsFile:
    # 文件夹 操作
    def __init__(self):
        pass
    # 获取文件夹下文件夹列表
    def getListdir(self, folder_path):
        path = Path(folder_path)
        return [subdir for subdir in path.iterdir() if subdir.is_dir()]

    # 获取文件夹下文件列表
    def getListfile(self, folder_path):
        path = Path(folder_path)
        return [subfile for subfile in path.iterdir() if subfile.is_file()]

    # 移动文件
    def rename(self, old_path, new_path):
        try:
            os.rename(old_path, new_path)
            print(f'success & 移动成功：{old_path} ---> {new_path}')
        except Exception as e:
            print(f'fail & 移动失败：{old_path} ---> {new_path}')
            print(f'失败原因：{e}')

    # 获取视频 或 图片
    def get_file_fullname(self,parent_path, stem, type='video'):
        video_suffix_list = ['.mp4', '.wmv', '.avi', '.mkv', '.ts', '.flv', '.mpeg']
        image_suffix_list = ['.jpg', '.jpeg', '.png', '.webp', '.ico']
        listarr = video_suffix_list
        if type == 'image':
            listarr = image_suffix_list

        fullpath = ''
        for item in listarr:
            fullpath = Path(parent_path) / (stem + item)
            if fullpath.exists():
                return fullpath
        return fullpath


myOsFile = MyOsFile()


class MyFileOption():
    # 文件 读写 操作
    def __init__(self):
        pass

    # 写入文件
    def write(self, file_path, file_data):
        try:
            with codecs.open(file_path,'w', encoding='utf-8') as f:
                f.write(file_data)
                print(f'success & 写入成功：{file_path}')
            return True
        except Exception as e:
            print(f'fail & 写入失败：{file_path}')
            print(f'失败原因：{e}')

    # 读取文件
    def read(self, file_path, file_data):
        try:
            with codecs.open(file_path,'r',  encoding='utf-8') as f:
                f.read(file_data)
                print(f'success & 读取成功：{file_path}')
            return True
        except Exception as e:
            print(f'fail & 读取失败：{file_path}')
            print(f'失败原因：{e}')

    # 读取xml为json
    def read_xml_to_json(self, xml_file_path):
        if os.path.exists(xml_file_path):
            with open(xml_file_path, 'r', encoding='utf-8') as file:
                xml_data = file.read()
            root = ET.fromstring(xml_data)
            movie_info = {}
            for child in root:
                movie_info[child.tag] = child.text
            return movie_info
        return None

    # 读取ini数据为json
    def ini_to_json(self, ini_file_path):
        config = configparser.ConfigParser()
        config.read(ini_file_path)

        data = {}
        for section in config.sections():
            data[section] = {}
            for option in config.options(section):
                data[section][option] = config.get(section, option)

        return json.dumps(data, indent=4)

    # json 转为 ini
    def json_to_ini(self, ini_file_path, json_data):
        data_dict = json_data
        config = configparser.RawConfigParser()

        # 将字典数据写入配置对象
        for section, options in data_dict.items():
            config.add_section(section)
            for option, value in options.items():
                config.set(section, option, value)

        # 将配置对象写入.ini 文件
        with open(ini_file_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

    # 创建nfo文件
    def write_nfo(self, json_data, nfo_path):
        pass


myFileOption = MyFileOption()


class MyApiOption:
    def __init__(self):
        pass

    def down_image(self, image_url, local_path, referer_url=''):
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
            if  response.status_code == 404:
                print('图片404')
                return False
            else:
                retry_count += 1
                cprint(f"---> HTTP错误: {response.status_code}，正在进行第 {retry_count + 1} 次重试，等待3秒...",
                       'red')
        cprint(f'---> 达到最大重试次数，文件下载失败', 'red')
        return False


    def jsonapi(self, link, jsonpath):
        pass


myApiOption = MyApiOption()


class DataFormat:
    def __init__(self):
        pass

    def hasattr(self, obj, key, default = ''):
        value = default
        if key in obj:
            value = obj[key]
        return value

dataFormat = DataFormat()


class LocalVideoFormat:
    def __init__(self):
        self.movieInfo = ''
        self.old_path = ''
        self.new_path = ''

    def init(self,old_path, new_path,  movie_info):
        self.new_path = new_path
        self.old_path = old_path
        self.movieInfo = movie_info
        self.play()

    def play(self):
        dirname = self.movieInfo['filename']
        pattern = r'[\\/:\*?"<>|]' # 不符合文件命名的字符串
        dirname = re.sub(pattern, ' ', dirname)
        dirname = re.sub(r' +', ' ', dirname).strip()

        dir_path = Path(self.new_path) / dirname
        ini_file = Path(self.new_path) / dirname / 'data.ini'
        nfo_file = Path(self.new_path) / dirname / f'{dirname}.nfo'
        thumb_file = Path(self.new_path) / dirname / 'poster.png'
        # 创建文件夹
        if not dir_path.exists():
            dir_path.mkdir()

        # 存到 db
        mysqlite3.myDBOption.connect_to_database()
        mysqlite3.myDBOption.insert_data(self.movieInfo)
        mysqlite3.myDBOption.close_to_database()

        # 创建 ini
        tempObj = {'MovieInfoc': self.movieInfo}
        myFileOption.json_to_ini(ini_file, tempObj)

        # 创建 nfo
        xml_data = self.get_nfo_data()
        myFileOption.write(nfo_file, xml_data)

        # 移动视频
        suffix = self.old_path.suffix
        new_video_url = Path(self.new_path) / dirname / f'{dirname}{suffix}'
        myOsFile.rename(self.old_path, new_video_url)

        # 下载海报
        image_remote_url = self.movieInfo['thumb']
        if 'referer' in self.movieInfo.keys():
            myApiOption.down_image(image_remote_url, thumb_file,  self.movieInfo['referer'])
        else:
            myApiOption.down_image(image_remote_url, thumb_file,'')

    def get_nfo_data(self):
        title = self.movieInfo['title']
        desc = self.movieInfo['desc']
        num = self.movieInfo['carno']
        release = self.movieInfo['release']
        studio = self.movieInfo['maker']
        actorList = self.movieInfo['actor'].split('、')
        series = self.movieInfo['series']
        website = self.movieInfo['website']
        actorStr = ''
        for item in actorList:
            actorStr += f'\n\t<actor>{item}</actor>'
        xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<movie>
    <num>{num}</num>
    <release>{release}</release>
    <title>{title}</title>{actorStr}
    <plot>{desc}</plot>
    <studio>{studio}</studio>
    <genre>{series}</genre>
    <thumb>poster.jpg</thumb>
    <website>{website}</website>
</movie>
'''
        return xml