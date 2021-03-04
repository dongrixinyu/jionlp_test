# -*- coding=utf-8 -*-
# 统计所有数据源中，词汇（包括汉语、外来常用语PUA等）的数量与分布概率

import os
import pdb
import json
import jieba
import multiprocessing as mp
import jionlp as jio

file_list = ['all_texts_1.txt', 'all_yuqing_3.txt', 'cctv_news.txt',
             'guoxin_rongyu_new_samples.txt', 'news_sic_weibo',
             'all_texts_2.txt',  'all_yuqing_4.txt',
             'guoxin_news_data',  'news_sic_wechat', '人民留言板.json']


def stat_func(file_name):
    word_dict = dict()
    if file_name == 'guoxin_rongyu_new_samples.txt':
        for line in jio.read_file_by_iter(
                os.path.join(dir_path, file_name), strip=False):
            for word in jieba.lcut(line[20:], use_paddle=True):
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict.update({word: 1})
    elif file_name == 'cctv_news.txt':
        for line in jio.read_file_by_iter(
                os.path.join(dir_path, file_name), strip=False):
            for word in jieba.lcut(line[9:], use_paddle=True):
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict.update({word: 1})
    elif file_name in ['人民留言板.json', 'news_sic_wechat', 'news_sic_weibo']:
        for line in jio.read_file_by_line(
                os.path.join(dir_path, file_name), auto_loads_json=True,
                strip=False):
            for word in jieba.lcut(''.join(line['main']), use_paddle=True):
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict.update({word: 1})
    else:
        # with open(os.path.join(dir_path, file_name), 'r', encoding='utf-8') as f:
        for line in jio.read_file_by_iter(
                os.path.join(dir_path, file_name), strip=False):
            for word in jieba.lcut(line, use_paddle=True):
                if word in word_dict:
                    word_dict[word] += 1
                else:
                    word_dict.update({word: 1})

    total_num = sum(list(word_dict.values()))
    word_tuple = sorted(word_dict.items(), key=lambda i:i[0])
    with open('word_count' + file_name, 'w', encoding='utf-8') as f:
        for item in word_tuple:
            f.write(json.dumps(list(item), ensure_ascii=False) + '\n')


dir_path = '/home/cuichengyu/text_dataset'
for file_name in file_list:
    print(file_name)
    p = mp.Process(target=stat_func, args=(file_name, ))
    p.start()

print('finished.')














