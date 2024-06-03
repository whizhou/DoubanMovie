# 使用requests库爬取电影信息并保存到 MovieInfo_str.csv

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
    while 1:
        try:
            res = requests.get(url, headers=head, timeout=30)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            return res
        except:
            print('getHtml: request Error')
            continue


# 处理日期格式
def parse_date(date_str) -> datetime:
    """
    尝试使用不同格式解析日期
    :param date_str:
    :return:
    """
    date_formats = ['%Y-%m-%d', '%Y', '%Y-%m', '%m', '%m-%d']
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue


# 爬取单个电影信息
def get_movie(url) -> list:
    """
    爬取单个电影的信息(除短评), 预处理成合适的字符串, 返回字符串列表
    :param url:
    :return:
    """
    # 下载网页并解析
    res = getHtml(url)
    bs = BeautifulSoup(res.text, 'html.parser')

    name = bs.find('span', property='v:itemreviewed').text

    year_str = bs.find('span', class_='year').text
    # year = int(year_str[1:-1])  # str2num '(1999)' -> 1999
    # print("%s (%d)" % (name, year))

    # info = bs.find_all('div', id='info')
    director = bs.find('a', rel="v:directedBy").text

    writer_span = bs.find('span', string='编剧')
    if writer_span:
        writers_set = writer_span.find_next('span', class_='attrs').find_all('a')
        writers_str = '/'.join([writer.get_text() for writer in writers_set])
    else:
        # 纪录片没有编剧，需要判断否则抛出 AttributeError
        print("There is no writer")
        writers_str = ''
    # 转换为字符串
    # print(scriptwriters)

    actor_set = bs.find_all('a', rel='v:starring')
    actors_str = '/'.join([actor.get_text() for actor in actor_set])
    # 转换为字符串
    # print(actors)

    type_set = bs.find_all('span', property='v:genre')
    types_str = '/'.join([movie_type.get_text() for movie_type in type_set])
    # print(types)

    region_span = bs.find('span', string='制片国家/地区:')
    region_set = region_span.next_sibling
    regions_str = '/'.join([region.strip() for region in region_set.split('/')])
    # print(regions)

    language_span = bs.find('span', string='语言:')
    language_str = language_span.next_sibling
    # languages = [language.strip() for language in language_set.split('/')]
    # print(languages)

    date_set = bs.find_all('span', property='v:initialReleaseDate')
    dates_locations_str = '/'.join([date.get_text() for date in date_set])
    # dates = []  # 初始化 dates 空列表
    # for item in dates_locations:
    #     # 找到左右括号位置
    #     left_paren_index = item.find('(')
    #     right_paren_index = item.find(')')
    #
    #     # 提取日期字符串并装换为 datetime 对象
    #     date_str = item[:left_paren_index]
    #     date = parse_date(date_str)
    #
    #     # 提取地点字符串
    #     location = item[left_paren_index + 1:right_paren_index]
    #
    #     # 添加到 dates 嵌套列表
    #     dates.append([date, location])
    # print(dates)

    # 爬取首个片长信息
    length_str = bs.find('span', property='v:runtime').text
    # length = int(length_str[0:length_str.find('分钟')])
    # print(length)

    rating_str = bs.find('strong', class_='ll rating_num', property='v:average').text
    # rating = float(rating_str)
    rating_people_str = bs.find('span', property='v:votes').text
    # rating_people = int(rating_people_str)
    # print(f"评分:{rating}, {rating_people}人评价")

    ratings_on_weight = bs.find('div', class_='ratings-on-weight').find_all('span', class_='rating_per')
    stars_str = '/'.join([star.get_text() for star in ratings_on_weight])
    # stars = [star_str[0:-1] for star_str in stars_str]
    # print(stars)

    return [name, year_str, director, writers_str, actors_str, types_str, regions_str, language_str,
            dates_locations_str, length_str, rating_str, rating_people_str, stars_str]


# TODO 爬取所有电影信息并保存到 data.csv
def get_all_movie_urls() -> list:
    """
    从分类界面(每页25部)获取每部电影链接, 汇总返回 list
    :return: list
    """
    movie_urls = []  # 创建空列表存储所有电影链接
    top250url = 'https://movie.douban.com/top250'
    # 不断爬取单页信息知道最后一页
    while top250url:
        # 爬取单页所有电影信息
        # 下载网页并解析
        res = getHtml(top250url)
        bs = BeautifulSoup(res.text, 'html.parser')

        # 找到所有电影链接并添加到列表
        movies_set = bs.find_all('div', class_='pic')
        movie_urls.extend([movie.find('a')['href'] for movie in movies_set])

        # 如果有下一页就切换到下一页
        top250url = bs.find('link', rel='next')
        if top250url:
            top250url = 'https://movie.douban.com/top250' + top250url['href']

    return movie_urls


movieUrls = get_all_movie_urls()
# print(len(movieUrls))

test_urls = [
    'https://movie.douban.com/subject/26430107/',
    'https://movie.douban.com/subject/1292052/',
    'https://movie.douban.com/subject/1291546/',
    'https://movie.douban.com/subject/1292720/',
    'https://movie.douban.com/subject/1292722/',
    'https://movie.douban.com/subject/1291561/',
    'https://movie.douban.com/subject/1292063/'
]
# movieInfo = []
# for test_url in test_urls:
#     movieInfo.append(get_movie(test_url))
# print(movieInfo)

movieInfo = []
num = 0
for url in movieUrls:
    movieInfo.append(get_movie(url))
    num += 1
    print(f"Progress:{num}/250")

head = ['name', 'year', 'director', 'writers', 'actors', 'types', 'regions', 'languages', 'dates', 'length', 'rating',
        'rating_people', 'stars']
movieInfoDf = pd.DataFrame(movieInfo, columns=head, dtype=str)
movieInfoDf.to_csv('MovieInfo_str.csv', index=False, encoding='utf-8-sig')
print(movieInfoDf.head())

# getMovie(test_urls[0])
