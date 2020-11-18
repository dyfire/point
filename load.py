# -*- coding:utf-8 -*-
import chardet

if __name__ == '__main__':
    f = open('sogou')
    try:
        while True:
            rs = f.readline().split('\t')
            if rs:
                str = chardet.detect(rs[2].replace('[', '').replace(']', ''))
                print(chardet.detect(rs[2].decode('gbk').encode('utf8')))
                break
            else:
                break
    finally:
        f.close()

    # .encode("utf-8")
