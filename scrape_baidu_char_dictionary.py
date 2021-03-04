import requests
import os
import re
from pyquery import PyQuery as pq
import jionlp

url_format = 'https://hanyu.baidu.com/s?wd={}&ptype=zici#basicmean'


res = requests.get(url_format.format('乲'))
# print(res.text)


def parse_html(html, char):
    doc = pq(html)
    radical_selector = '#radical > span'
    pinyin_selector = '#pinyin > span > b'
    traditional_selector = '#traditional > span'
    wubi_selector = '#wubi > span'
    basic_content_selector = '#basicmean-wrapper > div.tab-content'

    pinyin_list = doc(pinyin_selector).text()
    radical = doc(radical_selector).text()
    traditional = doc(traditional_selector).text()
    wubi = doc(wubi_selector).text()

    basic_content = doc(basic_content_selector).text()

    if ' ' in pinyin_list:
        pinyin_list = pinyin_list.split(' ')
    else:
        pinyin_list = [pinyin_list]

    basic_means = dict()
    # 'àáāǎòóōǒèéēěìíīǐùúūǔǜǘǖǚǹńňü'
    pinyin_ptn = re.compile('\[[a-zàáāǎòóōǒèéēěìíīǐùúūǔǜǘǖǚǹńňü ]{2,8}\]')
    explanation_ptn = re.compile('\d\.')
    # for
    res = pinyin_ptn.split(basic_content)
    # print(res)
    res = [item for item in res if item != '']

    if len(res) != len(pinyin_list):
        print(char, ': mistake')

    store_content = list()
    for pinyin_item, pinyin in zip(res, pinyin_list):
        explanations = explanation_ptn.split(pinyin_item)
        explanations = [item.replace('\n', '') for item in explanations if item not in ['', '\n']]
        # print(explanations)
        basic_means.update({pinyin: explanations})
        store_content.append('[')
        store_content.append(pinyin)
        store_content.append(']')
        for idx, i in enumerate(explanations):
            store_content.append(str(idx + 1))
            store_content.append('.')
            store_content.append(i)

    return '\t'.join([char, radical, traditional, wubi, ''.join(store_content)]), basic_content


def check_char_exception(line):
    num_ptn = re.compile('\d\.')

    if '日本汉字' in line or '日本用汉字' in line or '日本地名' in line or '日本和字' in line:
        # print(line.strip())
        return False
    if '韩国汉字' in line or '韩用汉字' in line or '韩国地名' in line or '〈韩〉' in line or '韩国字' in line or '韩文吏读字' in line:
        # print(line.strip())
        return False
    if '义未详' in line and len(line) < 30:
        # print(line.strip())
        return False
    if '〈韓〉' in line:
        # print(line.strip())
        return False

    if ('古同' in line or '古代' in line or '古书' in line or '古通' in line) and len(line.split('\t')[-1]) < 20:
        # print(line.strip())
        return False
    if ('古同' in line or '古代' in line or '古书' in line or '古通' in line) and len(line.split('\t')[-1]) >= 20:
        explanations = num_ptn.split(line.split('\t')[-1])[1:]
        explanations = [item.replace('\n', '') for item in explanations if item not in ['', '\n']]

        match_flag = True
        for i in explanations:
            if '古同' not in i and '古代' not in i and '古书' not in i and '古通' not in i:
                match_flag = False
                break
        if not match_flag:
            # print(line.strip())
            pass
        else:
            # print(line.strip())
            return False

    return True




q = parse_html(res.text, '得')
print(q)

f_all_info = open('all_info.txt', 'w', encoding='utf-8')
f_basic = open('basic_info.txt', 'w', encoding='utf-8')

for i in range(19968, 40870):
    res = requests.get(url_format.format(chr(i)))
    all_info, basic_content = parse_html(res.text, chr(i))
    if check_char_exception(all_info):
        f_all_info.write(all_info + '\n')
        f_basic.write(char + '\t' + basic_content + '\n')
    else:
        print(chr(i))


f_all_info.close()
f_basic.close()


