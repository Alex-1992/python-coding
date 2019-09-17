"""
    测试BeautifulSoup和lxml解析速度
    下载网页源代码到本地(避免网络波动影响)，分别用两种工具测试多次
"""

import requests
import time
import os
from lxml import etree
from bs4 import BeautifulSoup


def lxml_parse(_html_text, num):  # lxml解析函数
    selector = etree.HTML(_html_text)
    # 在循环测试性能前先解析一次，测试数据是否正确
    result = selector.xpath('//*[@id="w0"]/table/tbody/tr/td[2]/a/div/text()')  # 后面加的/text()是获取标签中的文本信息
    if not result:
        raise RuntimeError('error occurs when lxml parse data!')

    # 解析结果正确，开始循环解析，由于是测试性能，不用赋值接收
    print('lxml解析数据中...')
    for i in range(0, num):
        selector.xpath('//*[@id="w0"]/table/tbody/tr/td[2]/a/div/text()')


def bs_parse(_html_text, num):  # BeautifulSoup解析函数
    soup = BeautifulSoup(_html_text, 'lxml')
    # 在循环测试性能前先解析一次，测试数据是否正确
    result = soup.find_all('div', class_="text-success company pull-left")
    if not result:
        raise RuntimeError('error occurs when BeautifulSoup parse data!')

    # 解析结果正确，开始循环解析，由于是测试性能，不用赋值接收
    print('BeautifulSoup解析数据中...')
    for i in range(0, num):
        soup.find_all('div', class_="text-success company pull-left")


def get_test_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.131 '
                      'Safari/537.36 '
    }
    url = 'https://xjh.haitou.cc/xa/after'
    response = requests.get(url, headers=headers)
    with open('data/test_data.txt', 'w', encoding='utf-8') as _f:
        _f.write(response.text)


if __name__ == '__main__':  # 主程序入口
    # 首先判断一下有没有测试数据，没有的话直接到网页抓取下来存储到本地
    # 避免在后面的速度测试中受到网络波动的影响
    if not os.path.exists('data/test_data.txt'):
        get_test_data()

    # 分别用两个工具解析测试数据，对比速度
    repeat_time = 1000  # 测试次数
    with open('data/test_data.txt', 'r', encoding='utf-8') as f:
        html_text = f.read()
        # 首先测试BeautifulSoup
        start_time = time.time()
        bs_parse(html_text, 1000)
        end_time = time.time()
        print('BeautifulSoup解析 %d 次，耗时：%.10f ' % (repeat_time, end_time - start_time))

        # 测试lxml
        start_time = time.time()
        lxml_parse(html_text, 1000)
        end_time = time.time()
        print('lxml解析 %d 次，耗时：%.10f ' % (repeat_time, end_time - start_time))
"""
测试结果：
    BeautifulSoup解析 1000 次，耗时：5.6342358589 
    lxml解析 1000 次，耗时：1.1163809299 

BeautifulSoup与lxml对比：
    性能 lxml >> BeautifulSoup
    BeautifulSoup是基于DOM的，会载入整个文档，解析整个DOM树，时间和内存开销比较大，lxml只会局部遍历。
    lxml是用C语言写的，BeautifulSoup是用python写的，性能差很多
    易用性：
    BeautifulSoup > lxml
    BeautifulSoup的API比较人性化，支持css选择器。lxml的XPath写起来比较麻烦，开发效率不如BeautifulSoup。

总结：
    需求确定，要求性能的场合用lxml，快速开发用BeautifulSoup
"""
