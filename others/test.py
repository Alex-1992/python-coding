import os
import urllib
from urllib import request
import  requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# headers = {'user-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
# proxies = {'http':'120.220.220.95:8085'}
#
# # res = requests.get(url = 'https://www.baidu.com',headers= headers,proxies =proxies)
# # print(res.text)
# # with open("daili.html", 'w', encoding='utf-8')as f:
# #      f.write(res.text)
#
# from selenium import webdriver
#
# chromeOptions = webdriver.ChromeOptions()
# url = "http://www.baidu.com"
# # 设置代理
# chromeOptions.add_argument("--proxy-server=http://202.20.16.82:10152")
# # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
# browser = webdriver.Chrome('../spider/chromedriver',chrome_options=chromeOptions)
# #
# browser.get(url)
# # # 查看本机ip，查看代理是否起作用
# # browser.get("http://httpbin.org/ip")
# print(browser.page_source)
#
# # 退出，清除浏览器缓存
# browser.quit()
from selenium import webdriver


# options = webdriver.ChromeOptions()
# options.add_argument('--proxy-server=http://202.20.16.83:9657')
# driver = webdriver.Chrome('../spider/chromedriver',chrome_options=options)
# driver.get(url)
# print(driver.title)
#
# from selenium import webdriver
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=106.15.197.250:8001')
# chrome = webdriver.Chrome('../spider/chromedriver',chrome_options=chrome_options)
# chrome.get('http://www.huaban.com')
# print(chrome.page_source)
# chrome.quit()
os.mkdir('./111.txt')
