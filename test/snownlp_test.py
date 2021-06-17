from snownlp import SnowNLP
from jieba import analyse

def main():
    sss = '我每天最大的爱好就是看妞儿，因为看妞儿。可以让我心情愉悦！'
    res = SnowNLP(sss)
    # print(res.sentiments)
    # print(res.words)
    # print(res.tf)
    # print(res.idf)
    # print(res.pinyin)
    # print(res.sentences)
    # keywords = res.keywords(10)
    # print(str(keywords).replace("'", '"'))
    # tags = res.tags
    # for tag in tags:
    #     print(tag)

    jieba_res = analyse.extract_tags(sss)
    print(jieba_res[0:3])

if __name__ == '__main__':
    main()
