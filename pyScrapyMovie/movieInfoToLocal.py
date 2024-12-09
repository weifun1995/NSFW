# 刮削影片信息到本地
# 1：一般媒体库需要的.nfo文件
# 2：备份一份数据到本地.ini文件（因为.nfo文件经常打开会乱码,so 需要一个.ini转.nfo的函数）
# 3：备份一份数据到sqlite.db可以追溯

from aTools import utils, mysqlite3, maker

# 写入 .ini 文件
# 旧数据归档
# a.读取nfo文件 - b.写入。ini和.db

def read_oldfile_indb(folder_path):
    dirs = utils.myOsFile.getListdir(folder_path)
    mysqlite3.myDBOption.connect_to_database()
    for index, subdir in enumerate(dirs):
        print(index ,'\n当前目录', subdir, '名称', subdir.name)
        nfo_path = subdir.parent / subdir.name / (subdir.name + '.nfo')
        ini_path = subdir.parent / subdir.name / 'data.ini'
        nfo_data = utils.myFileOption.read_xml_to_json(nfo_path)
        print('原始数据', nfo_data)
        if not nfo_data:
            print('没有nfo数据')
            continue
        # old_filename = utils.myOsFile.get_file_fullname(subdir, subdir.name, 'video')

        # obj = maker.allMaker.av_10mu(nfo_data)
        obj = maker.allMaker.got2pee(nfo_data)
        # print(obj)
        # break

        if not obj['carno'] or not obj['release']:
            print('没有车牌号, 应该是没有归档好')
            continue

        obj['filename'] = subdir.name
        print('新数据', obj)

        # new_filename = obj['filename']
        # print(new_filename)
        #
        # suffix = old_filename.suffix
        #
        # old_filename_x = str(old_filename).replace(subdir.name, new_filename)
        # nfoFile = str(old_filename).replace(suffix, '.nfo')
        # nfoFile_x = nfoFile.replace(subdir.name, new_filename)
        # dirFile = str(old_filename.parent)
        # dirFile_x = dirFile.replace(subdir.name, new_filename)
        # ini_path = str(ini_path).replace(subdir.name, new_filename)
        #
        # utils.myOsFile.rename(dirFile, dirFile_x)``````````````````````````````````````````````
        # utils.myOsFile.rename(old_filename, old_filename_x)
        # utils.myOsFile.rename(nfoFile, nfoFile_x)
        #
        # obj['filename'] = obj['filename']

        ini_data = {'MovieInfo': obj}

        utils.myFileOption.json_to_ini(ini_path, ini_data)
        mysqlite3.myDBOption.insert_data(obj)




if __name__ == "__main__":
    read_oldfile_indb(r'E:\AV媒体库【E】\got2pee.com 29.09.2020-31.12.2021')
    pass