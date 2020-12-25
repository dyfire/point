#!/usr/bin/python
# -*-coding:utf-8-*-

import requests
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')


base_uri = dev_uri


def route(path):
    return base_uri + path


def create():
    try:
        url = route('register')

        while True:
            line = f.readline()
            if line:
                username, email = line.split(',')
                if email and username:
                    email = email[0:email.find('@')]

                    body = {
                        "data": {
                            "type": "users",
                            "attributes": {
                                "username": username,
                                "nickname": username,
                                "password": "123456",
                                "register_reason": "reason"
                            }
                        }
                    }

                    res = requests.post(
                        url,
                        json=body,
                        headers=headers
                    )

                    if res.text:
                        data = json.loads(res.text, encoding="gbk")

                        if data.has_key('errors'):
                            print('{} failure {}').format(username, data['errors'][0]['detail'][0])
                        else:
                            if data['data']['id'] > 0:
                                print "%s create success" % username
                            else:
                                print "%s create failure" % username
                    else:
                        print "%s create failure" % username
            else:
                break
    finally:
        f.close()
        print('finished')


def login(username, password):
    url = route('login')

    body = {
        "data": {
            "attributes": {
                "username": username,
                "password": password
            }
        }
    }

    res = requests.post(
        url,
        json=body,
        headers=headers
    )

    if res.text:
        data = json.loads(res.text, encoding="gbk")
        if data.has_key('errors'):
            print('failure {}').format(data['errors'][0]['detail']['message'])
            return False
        else:
            return data['data']
    else:
        return False


def find(**args):
    url = route('users?')
    str = ''
    print(args)
    for k, v in args.items():
        str += 'filter[%s]=%s' % (k, v)
    url += str

    res = requests.get(
        url,
        headers=headers
    )

    if res.text:
        data = json.loads(res.text, encoding="gbk")
        if data.has_key('errors'):
            print('failure {}').format(data['errors'][0]['detail']['message'])
            return False
        else:
            return data['data']
    else:
        print "find user failure"
        return False


def update(id, username):
    body = {
        "data": {
            "attributes": {
                "username": username,
                "password": '123456',
                "newPassword": '111111',
                'password_confirmation': '111111'
            }
        }
    }

    url = route('users/') + str(id)
    return requests.patch(
        url,
        json=body,
        headers=headers
    )


if __name__ == "__main__":
    headers = {
        'Accept': 'application/vnd.api+json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'authorization': dev_authorization
    }

    f = open('user.csv', 'rb')

    username = "汪建文"
    user = login(username, password)
    if user and len(user) > 0:
        id = user[0]['attributes']['id']
        if id > 0:
            res = update(id, username)
            print res.text
