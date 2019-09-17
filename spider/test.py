import jieba.analyse
import pyecharts.options as opts
from pyecharts.charts import WordCloud

targetTxt = './data/boss_job_detail.txt'
with open(targetTxt, 'r') as file:
    text = file.read()
text = text.replace('爬虫', '').replace('数据', '').replace('技术', '').replace('网页', '')
keywords = jieba.analyse.extract_tags(
    str(text), topK=20, withWeight=True, allowPOS=(['n']))
"""
参数解释：
* text : 待提取的字符串类型文本
* topK : 返回TF-IDF权重最大的关键词的个数，默认为20个
* withWeight : 是否返回关键词的权重值，默认为False
* allowPOS : 包含指定词性的词，默认为空,此处只取 'n'，表示过滤掉词性为名词之外的词
"""
print(keywords)

print('提取完毕！')
chart = WordCloud()
chart.add('技能需求频率', data_pair=keywords, word_size_range=[30, 200], shape='star')
chart.set_global_opts(title_opts=opts.TitleOpts(title='python职位需求技能'), tooltip_opts=opts.TooltipOpts(is_show=True))
chart.render('python.html')
# import os
#
# path = './data/pics/'
# file_path_list = []
#
# for root, ds, fs in os.walk(path):
#     for f in fs:
#         # file_path_list.append(root+f)
#         src_pic = open(root+f, 'rb')
#         pic_data = src_pic.read()
#         tar_pic = open('./data/pics1/' +f,'wb')
#         tar_pic.write(pic_data)
#         src_pic.close()
#         tar_pic.close()
# print(f.read() )
# print(  file_path_list)
# for file_path in file_path_list:
#     src_pic = open(file_path,'rb')
#     pic_data = src_pic.read()
#     tar_pic = open('./data/pics1/'+)
# with open(path,"rb") as f:
#     f.read()
# print('普通方式读写%d次耗时：%.5f' % (100, (10 - 0)))
