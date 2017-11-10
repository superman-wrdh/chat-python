# -*- coding:utf-8 -*-
import requests
api_key = "d1e2647********8b07584a16549c2de"
api_url = "http://www.tuling123.com/openapi/api"


def send_msg(msg):
    msg = {
        "key": api_key,
        "info": msg
    }
    response = requests.post(url=api_url, json=msg)
    data = response.json()
    return data



