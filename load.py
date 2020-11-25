#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

if __name__ == '__main__':
    f = open('sogou', 'rb')
    try:
        writer1 = open('sogou.origin', 'a')
        with open('sogou.extend', 'a') as writer:
            while True:
                row = f.readline()
                if row:
                    rs = row.split('\t')
                    year = random.randint(2018, 2020)
                    month = random.randint(1, 12)
                    day = random.randint(1, 28)
                    hour = random.randint(1, 23)
                    rs[0] = '{0}-{1}-{2} {3}'.format(year, month, day, rs[0])
                    rs[2] = rs[2].decode('gbk', 'ignore').encode('utf-8').replace('[', '').replace(']', '')

                    if len(rs) > 4:
                        rs[4] = rs[4].replace('\r\n', '').replace('\n', '')
                        ret = rs[3].split(' ')
                        if len(ret) == 2:
                            rs[3] = ret[0]
                            order = ret[1]
                        else:
                            order = 0
                    else:
                        rs.append(str(random.randint(1, 100)))
                        order = 0

                    rs.append(str(order))
                    writer1.write('\t'.join(rs) + '\n')

                    rs.append(str(year))
                    rs.append(str(month))
                    rs.append(str(day))
                    rs.append(str(hour))
                    writer.write('\t'.join(rs) + '\n')
                else:
                    break
    finally:
        f.close()
        print('finished')
