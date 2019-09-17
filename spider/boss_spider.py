"""
    根据设定的信息搜索并筛选boss直聘对应的职位，每个职位打开其对应的页面再抓取职责详情，
    最后将抓取到的信息用 jieba 分词进行处理，最后用 pyecharts 做成词云图并保存成html。
    boss直聘的反爬手段较多，代码中使用了构造请求头，添加更新cookie，ip代理池并在请求网页时随机sleep，
    并且将每阶段爬取到的信息存放到本地，再次运行时将从本地加载，避免高频访问被加入黑名单。
"""
import os
import random
import jieba.analyse
import pyecharts.options as opts
from pyecharts.charts import WordCloud
from lxml import etree
from selenium import webdriver
import time
import jieba.analyse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import boss_spider_setting as bss


def get_init_data_and_save():
    job_name = bss.job_name
    city_code = bss.city_code
    url = r'https://www.zhipin.com/job_detail/?query={}&city={}'.format(job_name, city_code)

    # 为chrome模拟登录添加代理，否则容易被封ip，每次随机从ip_pool中选择
    chrome_options.add_argument("--proxy-server=" + random.choice(bss.ip_pool))
    browser = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

    # 为chrome模拟登录添加cookie
    for cookie in bss.cookies:
        browser.add_cookie(cookie)

    browser.get(url)
    # 等待页面中所需的元素全部加载完毕后再执行后面的代码
    WebDriverWait(driver=browser, timeout=10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'job-primary')))
    browser.quit()

    # 登录成功后保存cookie到本地
    bss.cookies = browser.get_cookies()

    # 将访问到的初始界面保存到本地
    with open(init_html_path, 'w', encoding='utf-8') as _f:
        _f.write(browser.page_source)

    # 将包含job粗略信息的div保存到列表
    _selector = etree.HTML(browser.page_source)
    # job_list = browser.find_elements_by_xpath('//div[@class="job-primary"]')[:job_num]
    global job_div_list
    job_div_list = _selector.xpath('//div[@class="job-primary"]')[0:bss.job_num]
    if not job_div_list:
        raise RuntimeError('获取job_div_list失败！请确保代理ip可正常使用')


def select_job_url_list():
    # 将包含关键字的job div处理，得到能拿到职位详情的url，存入job_url_list
    for job in job_div_list:
        if not isinstance(job, str):
            j = job.xpath('//*[@class="job-name"]/a')[0]
            _job_name = j.text
            # 根据工作名字判断是否包含keyword
            for key in bss.key_word:
                if key in _job_name:
                    job_link = j.attrib.get('href')
                    job_url_list.append('https://www.zhipin.com' + job_link)
    if not job_url_list:
        raise RuntimeError('获取job_url_list失败！')


def get_job_info_list():
    # 从job_url_list中得到每一个具体的url，并爬取职位详情保存到列表并返回列表
    print('共找到%d个相关职位信息,开始提取信息' % len(job_url_list))
    _list = []
    for index, _url in enumerate(job_url_list, 1):
        print('正在爬取第%d个职位信息......' % index)
        # 为chrome模拟登录添加代理，否则容易被封ip，每次随机从ip_pool中选择
        chrome_options.add_argument("--proxy-server=" + random.choice(bss.ip_pool))
        browser = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
        browser.get(_url)
        # 模拟人的操作，每次随机停顿，爬得太快容易被封
        time.sleep(random.randint(4, 8))
        browser.quit()
        res = etree.HTML(browser.page_source)
        job_info = str(res.xpath('//div[@class="text"]/text()'))
        job_info.replace('\n', '')
        _list.append(job_info)
    browser.close()
    if not _list:
        raise RuntimeError('获取job_info_list失败！')
    return _list


def save_detail_to_local():
    print('信息爬取完成，开始处理数据并写入文件')
    with open(job_detail_path, 'w') as target_file:
        for job_info in job_info_list:
            seg = jieba.cut(job_info.strip(), cut_all=False)
            # 用空格将分好的词连接成一行
            output = ' '.join(seg)
            target_file.write(output)
            target_file.write('\n')
    print('写入完成！')


def analyse_data():
    """
        参数解释：
        * text : 待提取的字符串类型文本
        * topK : 返回TF-IDF权重最大的关键词的个数，默认为20个
        * withWeight : 是否返回关键词的权重值，默认为False
        * allowPOS : 包含指定词性的词，默认为空,此处只取 'n'，表示过滤掉词性为名词之外的词
    """

    with open(job_detail_path, 'r') as file:
        text = file.read()
    text = text.replace('爬虫', '').replace('数据', '').replace('技术', '').replace('网页', '')
    keywords = jieba.analyse.extract_tags(
        str(text), topK=20, withWeight=True, allowPOS=(['n']))
    print('分析完毕!')
    return keywords


def visualize_data(_words):
    chart = WordCloud()
    chart.add('技能需求频率', data_pair=_words, word_size_range=[30, 200], shape='star')
    chart.set_global_opts(title_opts=opts.TitleOpts(title='python职位需求技能'),
                          tooltip_opts=opts.TooltipOpts(is_show=True))
    chart.render('./data/boss_data_result.html')
    print('可视化处理完成,结果保存至：/data/boss_data_result.html')


if __name__ == '__main__':

    job_url_list = []  # 用于存放每条职位对应的url
    job_div_list = []  # 存放job的div对象

    init_html_path = './data/boss_init_html.txt'  # 存放爬取到的母界面的路径
    job_detail_path = './data/boss_job_detail.txt'  # 存放爬取的具体职位信息的路径

    chrome_options = webdriver.ChromeOptions()
    if os.path.exists(init_html_path):
        if not os.path.exists(job_detail_path):
            print('不存在已经爬取过的职位详情，但存在指向爬取职位详情的母页面')
            with open(init_html_path, 'r', encoding='utf-8') as f:
                # 从本地读取文件并得到job_div_list
                html_text = f.read()
                selector = etree.HTML(html_text)
                job_div_list = selector.xpath('//div[@class="job-primary"]')[0:bss.job_num]
                # 在job_div_list中挑选job_title中有keyword的job信息并将链接保存至job_url_list
                select_job_url_list()
                # 根据job_url_list中的每个url到具体界面拿到职位详情并保存至job_info_list
                job_info_list = get_job_info_list()
                # 将job_info_list中的数据保存到本地
                save_detail_to_local()
        else:
            print('存在已经爬取过的职位详情，直接分析')
    else:
        print('不存在任何爬取过的数据，需要重新爬取')
        # 获得初始的访问数据并保存到本地，得到包含粗略job信息的job_div_list
        get_init_data_and_save()
        # 在job_div_list中挑选job_title中有keyword的job信息并将链接保存至job_url_list
        select_job_url_list()
        # 根据job_url_list中的每个url到具体界面拿到职位详情并保存至job_info_list
        job_info_list = get_job_info_list()
        # 将job_info_list中的数据保存到本地
        save_detail_to_local()
    # 从本地读取职位详情数据并分析，返回 关键字与出现频率
    words = analyse_data()
    # 将分析过的数据用pyecharts 可视化并保存本地html
    visualize_data(words)
