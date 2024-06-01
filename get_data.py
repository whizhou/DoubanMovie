# 使用requests库爬取电影信息

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


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
def getMovie(url) -> pd.Series:
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
    # print("%s (%d)" % (name, year))

    # info = bs.find_all('div', id='info')
    director = bs.find('a', rel="v:directedBy").text

    writer_span = bs.find('span', string='编剧')
    writers = writer_span.find_next('span', class_='attrs').find_all('a')
    scriptwriters = [writer.get_text() for writer in writers]
    print(scriptwriters)
    # scriptwriters = info.find('a', )
    # print(info)



# TODO 爬取所有电影信息并保存到 data.csv

test_urls = [
    'https://movie.douban.com/subject/1292052/',
    'https://movie.douban.com/subject/1291546/',
    'https://movie.douban.com/subject/1292720/',
    'https://movie.douban.com/subject/1292722/',
    'https://movie.douban.com/subject/1291561/',
]
for test_url in test_urls:
    getMovie(test_url)

# getMovie(test_urls[0])
