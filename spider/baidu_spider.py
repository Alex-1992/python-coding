import requests
from bs4 import BeautifulSoup
import lxml.html
from multiprocessing.dummy import Pool


def getDataSave(url):
    html_text = getHTMLText(url)
    selector = lxml.html.fromstring(html_text)
    content = selector.xpath('//div[starts-with(@id,"post_content")]/text()')
    print(content)
    for each in content:
        data_list.append(each)
        print(each)


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        # print(r.text)
        return r.text
    except:
        return ''


url = 'https://tieba.baidu.com/p/7032170047?pn='
url_list = []
data_list = []
for i in range(1, 11):
    url_list.append(url + str(i))
pool = Pool(5)
pool.map(getDataSave, url_list)
print(data_list)
# html_text = getHTMLText(url)
with open('data.txt', 'w', encoding='utf-8') as f:
    for d in data_list:
        print(d)
        print('---------')
        if d.length <= 3:
            continue
        f.writelines(d)
        f.write('\n')
    # f.write(str(data_list))
