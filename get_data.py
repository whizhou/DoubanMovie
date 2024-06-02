# 使用requests库爬取电影信息

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from datetime import datetime


# 下载网页
def getHtml(url) -> requests.Response:
    """
    :param url:
    :return requests.Response:
    """
    head = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    try:
        res = requests.get(url, headers=head, timeout=30)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        return res
    except:
        print('getHtml: request Error')


# TODO 爬取单个电影信息
def getMovie(url) -> list:
    """
    爬取单个电影的信息（除短评）
    :param url:
    :return:
    """
    # 下载网页并解析
    res = getHtml(url)
    bs = BeautifulSoup(res.text, 'html.parser')

    name = bs.find('span', property='v:itemreviewed').text

    year = bs.find('span', class_='year').text
    year = int(year[1:-1])  # str2num '(1999)' -> 1999
    # print("%s (%d)" % (name, year))

    # info = bs.find_all('div', id='info')
    director = bs.find('a', rel="v:directedBy").text

    writer_span = bs.find('span', string='编剧')
    writers_set = writer_span.find_next('span', class_='attrs').find_all('a')
    scriptwriters = [writer.get_text() for writer in writers_set]
    # 转换为字符串列表
    # print(scriptwriters)

    actor_set = bs.find_all('a', rel='v:starring')
    actors = [actor.get_text() for actor in actor_set]
    # 转换为字符串列表
    # print(actors)

    type_set = bs.find_all('span', property='v:genre')
    types = [movie_type.get_text() for movie_type in type_set]
    # print(types)

    region_span = bs.find('span', string='制片国家/地区:')
    region_set = region_span.next_sibling
    regions = [region.strip() for region in region_set.split('/')]
    # print(regions)

    language_span = bs.find('span', string='语言:')
    language_set = language_span.next_sibling
    languages = [language.strip() for language in language_set.split('/')]
    # print(languages)

    date_set = bs.find_all('span', property='v:initialReleaseDate')
    dates_locations = [date.get_text() for date in date_set]
    dates = [] # 初始化 dates 空列表
    for item in dates_locations:
        # 找到左右括号位置
        left_paren_index = item.find('(')
        right_paren_index = item.find(')')

        # 提取日期字符串并装换为 datetime 对象
        date_str = item[:left_paren_index]
        date = datetime.strptime(date_str, '%Y-%m-%d')

        # 提取地点字符串
        location = item[left_paren_index + 1:right_paren_index]

        # 添加到 dates 嵌套列表
        dates.append([date, location])
    # print(dates)


# TODO 爬取所有电影信息并保存到 data.csv


test_urls = [
    'https://movie.douban.com/subject/1292052/',
    'https://movie.douban.com/subject/1291546/',
    'https://movie.douban.com/subject/1292720/',
    'https://movie.douban.com/subject/1292722/',
    'https://movie.douban.com/subject/1291561/',
    'https://movie.douban.com/subject/1292063/'
]
for test_url in test_urls:
    getMovie(test_url)

# getMovie(test_urls[0])
