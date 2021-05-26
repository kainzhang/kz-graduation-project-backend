from snownlp import SnowNLP
import pandas as pd


def main():
    str = '这个电影好烂'
    s = SnowNLP(u'这个电影好烂')
    s1 = SnowNLP(str)
    print(s.sentiments)
    print(s1.sentiments)
    pass


if __name__ == '__main__':
    main()