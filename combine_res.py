# -*- coding=utf-8 -*-

import os
import json
import math
import jionlp as jio

dir_path = '/home/cuichengyu/text_dataset'
file_list = ['all_texts_1.txt', 'all_yuqing_3.txt', 'cctv_news.txt',
             'guoxin_rongyu_new_samples.txt', 'news_sic_weibo',
             'all_texts_2.txt',  'all_yuqing_4.txt',
             'guoxin_news_data',  'news_sic_wechat', '人民留言板.json']

char_dict = dict()
for file_name in file_list:
    for line in jio.read_file_by_line(os.path.join(dir_path, 'char_count' + file_name)):
        if line[0] in char_dict:
            char_dict[line[0]] += line[1]
        else:
            char_dict.update({line[0]: line[1]})

total_num = sum(list(char_dict.values()))
word_tuple = sorted(char_dict.items(), key=lambda i: i[0])
with open('char_count.txt', 'w', encoding='utf-8') as f:
    for item in word_tuple:
        prob = item[1] / total_num
        log_prob = - math.log10(prob)
        f.write(json.dumps([item[0], item[1], prob, log_prob], ensure_ascii=False) + '\n')












