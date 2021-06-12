import jieba
import re
from collections import Counter


def main():
    sss = '我每天#最大的1爱!!好就是*看妞儿，因为2看妞儿。24323。可以让我心情愉悦！'
    # pattern = re.compile('[^A-Z^a-z^0-9^\u4e00-\u9fa5]')
    pattern = re.compile('[^\u4e00-\u9fa5]')
    sssd = pattern.sub('', sss)
    words = jieba.cut(sssd)

    stop_words = [line.strip() for line in open('../data/stopwords.txt', encoding='utf-8').readlines()]

    word_list = []
    for word in words:
        if word not in stop_words:
            word_list.append(word)

    word_cnt = Counter(word_list)
    word_res = word_cnt.most_common(3)

    word_dict = dict(word_res)
    print(word_dict)

    data_str = ''
    for key in word_dict.keys():
        data_str += ('{name:"' + key + '",value:' + str(word_dict[key]) + '},')

    print(data_str)


if __name__ == '__main__':
    main()
