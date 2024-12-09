import time
from pathlib import Path

from termcolor import colored

from aTools import utils
from avScrapyer import getter_javdb,getter_javbus, getter_office_web, meta_data, meta_utils


def getter_dir_files(folder_path):
    directory = Path(folder_path)
    # .parent .name .stem .suffix
    return [file for file in directory.iterdir() if file.is_file()]


def do_scrapy_something(scrapy_filename):
    scrapy_filename = scrapy_filename.lower()
    sure_series = ''
    sure_carno = scrapy_filename
    sure_args = ''
    movie_info = None
    sure_function = ''
    alist = meta_data.maker_assert
    for aitem in alist:
        if aitem in scrapy_filename:
            sure_series = aitem
            sure_function = alist[aitem]['function']
            if 'args' in alist[aitem]:
                sure_args = alist[aitem]['args']
            arr =scrapy_filename.split('-')
            if len(arr) > 1:
                sure_carno = '-'.join(arr[1:])

    maker_flag_used = False # 是否已经启用了官网查询
    if sure_series:
        print('确定官网', sure_carno,sure_function, sure_args)
        my_makerScrapyer = getter_office_web.MakerScrapyer(sure_carno,sure_function, sure_args )
        movie_info = my_makerScrapyer.init()
        maker_flag_used = True
        if movie_info:
            print('官网爬取成功', '\n', movie_info)
            return movie_info

    # 进行javDB查询
    my_javdb = getter_javdb.JavDB(scrapy_filename)
    javdb_info = my_javdb.init()
    print('查询到的javdb信息', javdb_info)
    if javdb_info and 'series' in javdb_info:
        match_series = javdb_info['series']
        if match_series in meta_data.mapping_alias_list:
            temp = meta_data.mapping_alias_list[match_series]
            sure_series = temp['short']
            sure_function = alist[sure_series]['function']
            sure_args = alist[sure_series]['value']
            print('根据javDB推断官网:', sure_series)

    if sure_series and not maker_flag_used:
        my_makerScrapyer = getter_office_web.MakerScrapyer(sure_carno,sure_function, sure_args )
        movie_info = my_makerScrapyer.init()
        if movie_info:
            return movie_info

    # 确定官网没有信息就返回javDB的信息
    if javdb_info:
        return javdb_info

    # 爬取 javBus 信息
    my_javbus = None
    if not my_javbus:
        edge = meta_utils.EdgeDrive()
        driver = edge.open()
        my_javbus = getter_javdb.JavBus(driver)
    javbus_info = my_javbus.open_page('100824-001')
    return javbus_info


def do_scrapy_play(curr_filename):
    maker_scrapy_isNo_flag = True # 是否已经进行官网刮削（默认False）
    maker_tag = ''
    carno = curr_filename
    movie_info = None
    myMaker = getter_office_web.MakerScrapyer(curr_filename)
    maker_info = myMaker.init()
    if maker_info and maker_info != '没有实现函数':
        return maker_info

    if maker_info == '没有实现函数':
        maker_scrapy_isNo_flag = False

    if not movie_info:
        carno = myMaker.carno

        # myJavdb = getter_javdb.JavDB(curr_filename)
        # javdb_info = myJavdb.init()
        #
        # if not maker_scrapy_isNo_flag:
        #     # 如果没有进行官网爬取就重新爬取：
        #     temp_filename = javdb_info['maker'] + '-' + curr_filename
        #     temp_maker_nfo = getter_office_web.MakerScrapyer(temp_filename).init()
        #     if temp_maker_nfo:
        #         return temp_filename
        #
        # if javdb_info:
        #     return javdb_info


        # # 进行javbooks 爬取
        # myJavbus = None
        # # if not javdb_info and not myJavbus:
        # if not myJavbus:

        #
        # edge = meta_utils.ChromeDrive()
        # driver = edge.open()
        # myJavbus = getter_javbus.JavBus(driver)
        #
        # javbus_info = myJavbus.open_page(carno)
        # if javbus_info:
        #     return meta_utils.format_movie_info(javbus_info)

        return None




    # sure_args = ''
    # sure_function = ''
    # maker_info = None
    # alist = meta_data.maker_assert
    # for maker_item in maker_list:
    #     if maker_item in curr_filename:
    #         maker_tag = maker_item
    #         sure_function = alist[maker_item]['function']
    #         if 'args' in alist[maker_item]:
    #             sure_args = alist[maker_item]['args']
    #         arr = curr_filename.split('-')
    #         if len(arr) > 1:
    #             carno = '-'.join(arr[1:])
    #         else:
    #             print(f'文件命名错误，终端爬取操作：{curr_filename}')
    #             return
    #         break

    # if maker_tag:
    #     # 确定官网
    #     my_makerScrapyer = getter_office_web.MakerScrapyer(carno, sure_function, sure_args)
    #     movie_info = my_makerScrapyer.init()
    #     if not movie_info:
    #         print('爬取官网信息失败')
    #     print(movie_info)
    #     pass


def do_scrapy(folder_path):
    archive_folder_fail = Path(f'{folder_path}/刮削失败')  # 当前目录下创建的归档文件夹
    archive_folder_success = Path(f'{folder_path}/刮削成功')  # 当前目录下创建的归档文件夹
    if not archive_folder_fail.exists():
        archive_folder_fail.mkdir()
    if not archive_folder_success.exists():
        archive_folder_success.mkdir()
    # screens_folder = Path(f'{folder_path}/归档/screens')
    # if not screens_folder.exists():
    #     screens_folder.mkdir()

    # 文件列表
    av_files = getter_dir_files(folder_path)

    for index, item in enumerate(av_files): # 循环需爬取的视频
        time.sleep(2)
        print(item)
        carno = item.stem
        print('\n', colored(f'当前处理：{index + 1} / {len(av_files)}', 'yellow'))
        print(colored(f'-> 开始车号：{carno}', 'blue'))

        # movie_info = do_scrapy_something(carno)
        movie_info = do_scrapy_play(carno)
        print('修改前', movie_info)

        if movie_info:
            movie_info = meta_utils.format_movie_info(movie_info)
            print('修改后',  movie_info)
            # break
            # new_path = Path(r'E:\avplace\刮削结果')
            new_path = archive_folder_success
            formatter = utils.LocalVideoFormat()
            formatter.init(item, new_path, movie_info)
            # break

        # break
        # if not movie_info:
        #     cprint('-> 没有爬取到影片信息', 'red')
        #     continue
        #
        # filename = movie_info['filename']
        # pattern = r'[\\/:\*?"<>|]' # 不符合文件命名的字符串
        # filename = re.sub(pattern, ' ', filename)
        # filename = re.sub(r' +', ' ', filename).strip()
        # thumb = movie_info['thumb']
        # # 创建视频归档文件夹
        # local_video_folder = Path(f'{archive_folder}/{filename}')
        # if not local_video_folder.exists():
        #     local_video_folder.mkdir()
        #
        # # 下载海报
        # local_bigimg_url = f'{local_video_folder}/poster.png'
        # print('下载海报：', thumb, '<---->',  local_bigimg_url)
        #
        # downFlag = meta_utils.down_image(thumb, local_bigimg_url)
        # if not downFlag:
        #     cprint('-> 下载海报失败', 'red')
        #
        # new_bigimg_url = f'{screens_folder}/{filename}.png'
        #
        # try:
        #     shutil.copyfile(local_bigimg_url, new_bigimg_url)
        #     cprint("-> 图片复制成功", 'green')
        # except Exception as e:
        #     cprint("-> 图片复制失败", 'red')
        #
        # # 重命名视频
        # old_video_url = f'{item.parent}/{item.name}'
        # new_video_url = f'{local_video_folder}/{filename + item.suffix}'
        # cprint(f'-> {old_video_url} 移动到 {new_video_url} ', 'blue')
        # try:
        #     shutil.move(old_video_url, new_video_url)
        #     cprint("-> 移动成功", 'green')
        # except Exception as e:
        #     cprint("-> 移动失败", 'red')
        #     print(e)


if __name__ == "__main__":
#     query_has_image()
#     do_scrapy(r'E:\avplace\【图鉴】10mu-秘藏')
    do_scrapy(r'E:\avplace\【图鉴】マンコ図鑑（穴）')
    pass
