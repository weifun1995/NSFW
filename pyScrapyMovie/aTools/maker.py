
class AllMaker:
    def __init__(self):
        pass

    # 获取 obj属性值
    def hasattr(self, obj, key, default=''):
        value = default
        if key in obj and obj[key]:
            value = obj[key]
            value = value.replace('\n', '').strip()
        return value

    def get_general_data(self, objData):
        carno = self.hasattr(objData, 'num', '')
        desc = self.hasattr(objData, 'description', '')
        release = self.hasattr(objData, 'release', '')
        website = self.hasattr(objData, 'website', '')
        title = self.hasattr(objData, 'title', '')
        actor = self.hasattr(objData, 'actor', '')
        return {
            'carno': carno,
            'desc': desc,
            'release': release,
            'website': website,
            'title': title,
            'actor': actor,
        }

    def got2pee(self, objData):
        general_data = self.get_general_data(objData)
        key = general_data['website'].split('/')[-2].lower()
        thumb = f'https://media.got2pee.com/videos/{key}/cover/hd.jpg'
        maker = 'got2pee.com'
        series = ''
        type = 'pee'
        tags = 'pee、outdoor、小便、尿尿、户外'

        id = f'got2pee.{general_data["release"]}.{key}'

        obj = {
            'id': id,
            'thumb': thumb,
            'type': type,
            'tags': tags,
            'maker': maker,
            'series': series,
        }
        general_data.update(obj)
        return general_data

    def av_10mu(self, objData):
        general_data = self.get_general_data(objData)
        print('\n', )
        id = f'10musume.{general_data["release"]}.{general_data["carno"]}'
        thumb = f'https://www.10musume.com/assets/sample/{general_data["carno"]}/str.jpg'
        maker = '10musume.com'
        series = '秘蔵マンコセレクション'
        type = '図鑑'
        tags = '図鑑、女体、阴道、屄、pussy'
        timer = general_data["release"].replace('-', '.')
        website = f'https://www.10musume.com/movies/{general_data["carno"]}/'
        if not general_data['actor']:
            general_data['actor'] = general_data['title'].split('_')[-1]
        filename = f'10musume.{timer}({general_data["carno"]}).{series}({general_data["actor"]})'
        obj = {
            'id': id,
            'thumb': thumb,
            'type': type,
            'tags': tags,
            'maker': maker,
            'series': series,
            'website': website,
            'filename': filename
        }
        general_data.update(obj)
        return general_data

allMaker = AllMaker()