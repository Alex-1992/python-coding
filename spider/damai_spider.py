import re
import lxml.html
from selenium import webdriver
import csv


def get_right_show_time(time_list):
    for _time in time_list:
        m = rep.search(_time)
        if m:
            # print(m.group())
            return m.group()


if __name__ == '__main__':
    # user_agent = 'Mozilla / 5.0(Macintosh;IntelMacOSX10_15_7) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / ' \
    #              '97.0.4692.99Safari / 537.36 '

    des_url = 'https://search.damai.cn/search.htm'
    driver = webdriver.Chrome('./chromedriver')
    driver.get(des_url)
    # 利用chromedriver模拟访问
    html = driver.page_source
    selector = lxml.html.fromstring(html)
    item_list = selector.xpath('//div[@class="items"]')
    # 得到所有class为items的元素列表 准备提取数据

    data_list = []
    rep = re.compile(r'([\d.-]){10,}')
    # 在这里编译正则对象 后面循环调用节省调用
    # 将日期与文字区分开来并提取日期 顺便去掉空格和换行符
    for item in item_list:
        show_place = item.xpath('div/div[@class="items__txt__title"]/span/text()')[0]
        # 解析后的字符串被放在一个list里，用[0]拿到
        show_name = item.xpath('div/div[@class="items__txt__title"]/a/text()')[0]

        show_time_list = item.xpath('div/div[@class="items__txt__time"]/text()')
        ''' time的提取稍微麻烦点 class为 items__txt__time 的元素有三个，不确定哪个是写数字的日期，
                   所以利用之前的定义的的正则判断一下，这里用一个方法处理
               '''
        show_time = get_right_show_time(show_time_list)

        show_price = item.xpath('div/div[@class="items__txt__price"]/span/text()')[0]
        item_dict = {'show_place': show_place if show_place else '',
                     'show_name': show_name if show_name else '',
                     'show_time': show_time if show_time else '',
                     'show_price': show_price if show_price else '',
                     }
        data_list.append(item_dict)

    with open('data/damai_result.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['show_place',
                                               'show_name',
                                               'show_time',
                                               'show_price'])
        writer.writeheader()
        writer.writerows(data_list)
