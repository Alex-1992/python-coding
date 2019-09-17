import requests
import re
import os


def get_html_text(url):
    r = requests.get(url)
    r.raise_for_status()
    if not r.text:
        raise RuntimeError('获取网页：%s 内容失败' % url)
    return r.text


def parse_pid(_html):
    # 拿出前100的 id 与 采集数
    # 取前10个放入list
    list_p = {}
    id_list = re.findall(r'"pin_id":\d+', _html)[:search_num]
    picklist = re.findall(r'"repin_count":\d+', _html)[:search_num]
    for i in range(0, len(id_list)):
        list_p[id_list[i].split(':')[1]] = picklist[i].split(':')[1]
    list_p = sorted(list_p.items(), key=lambda item: int(
        item[1]), reverse=True)
    list_p = list_p[:10]
    list_p = sorted(list_p, key=lambda item: int(
        item[1]), reverse=True)
    return list_p


def write_pic_data(k):
    pic_url = 'https://huaban.com/pins/' + k + '/'
    _html = get_html_text(pic_url)
    # reg = re.compile(pid + r'.*?", "type"$')
    reg1 = re.compile(r'"pin_id":' + k + r'.*?", "urlname"')
    str1 = reg1.search(_html).group(0)

    repin = re.search(r'"repin_count":\d+', str1).group(0).split(':')[1]
    like = re.search(r'"like_count":\d+', str1).group(0).split(':')[1]
    _type = re.search(r'"raw_text":"[^"]+', str1).group(0).split(':"')[1]
    name = re.search(r'"username":"[^"]+', str1).group(0).split(':"')[1]
    print(repin, like, _type, name)

    code = str1.split('"key":"')[1].split('", "type"')[0]
    down_url = 'https://hbimg.huabanimg.com/' + code
    r = requests.get(down_url)
    # coding:utf-8
    path = '主题:' + _type + '||画师:' + name + '||采集:' + repin + '||喜欢:' + like + '.png'
    path = re.sub(r'(?u)[^-\w.]', '_', path)

    with open(('data/pics/' + path), 'wb+') as f:
        f.write(r.content)


if __name__ == '__main__':

    # 1.https://huaban.com/search/?q=原画 搜索前一百个资源 根据采集次数排序取前10
    # 2.根据拿到的pid 去 https://huaban.com/pins/ + pid + /  找到主图code
    # 3.根据链接https://hbimg.huabanimg.com/ + code  下载主图片  保存下载的图片到本地
    # 4.根据  用户名 种类 采集数，喜欢数 作为文件名保存
    search_num = 100
    pick_num = 10
    key_word = '原画'

    # 每页最多拿100个 超过100会被限制成20
    start_url = 'https://huaban.com/search/?q=' + key_word + '&per_page=100'
    html = get_html_text(start_url)
    pid_list = parse_pid(html)

    if not os.path.isdir('data/pics'):
        os.mkdir('data/pics')
    print(pid_list)
    for k in pid_list:
        write_pic_data(k[0])
