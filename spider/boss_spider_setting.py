job_name = 'python爬虫'  # 可以改变搜索的关键字，例如搜索java开发
city_code = '101110100'  # 101110100表示 西安
url = r'https://www.zhipin.com/job_detail/?query={}&city={}'.format(job_name, city_code)
job_num = 30  # 要爬取的职位数量
key_word = ['爬虫']  # 爬取到的职位名字必须至少包含 keyword 其中的一个才会算入结果
ip_pool = ['http://120.220.220.95:8085',
           'http://106.15.197.250:80',
           'http://202.109.157.65:9000',
           'http://103.37.141.69:8001',
           ]
cookies = [
    {'domain': '.zhipin.com', 'httpOnly': False, 'name': '__c', 'path': '/', 'secure': False, 'value': '1648174220'},
    {'domain': '.zhipin.com', 'httpOnly': False, 'name': 'Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a', 'path': '/',
     'secure': False, 'value': '1648174220'},
    {'domain': '.zhipin.com', 'expiry': 1963534220, 'httpOnly': False, 'name': '__a', 'path': '/', 'secure': False,
     'value': '31642309.1648174220..1648174220.1.1.1.1'},
    {'domain': '.zhipin.com', 'expiry': 1648404619, 'httpOnly': False, 'name': '__zp_stoken__', 'path': '/',
     'secure': False,
     'value': '956fdGnl3GgR'
              '%2FKmpWUF8MFStMfQsfCD0ua2h1Bz0seDMlPmhhYVolAXJpaUduPCchQX9fCQxdXnRXbCU8LUMqJx8nFn0EeGZQLiVHcwxBM2IDGB'
              'tyfzh2QjMvdB4LNUFqA0ZtfQx9NANBfiE%3D'},
    {'domain': '.zhipin.com', 'httpOnly': False, 'name': '__g', 'path': '/', 'secure': False, 'value': '-'},
    {'domain': '.zhipin.com', 'httpOnly': False, 'name': 'lastCity', 'path': '/', 'secure': False,
     'value': '100010000'}, {'domain': '.zhipin.com', 'expiry': 1679710219, 'httpOnly': False,
                             'name': 'Hm_lvt_194df3105ad7148dcf2b98a91b5e727a', 'path': '/', 'secure': False,
                             'value': '1648174219'},
    {'domain': 'www.zhipin.com', 'expiry': 1648176018, 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'secure': False,
     'value': '0bcb2f1916481741353777908e7e833d535496b41a784a7c68f9ac592c4083'}]

