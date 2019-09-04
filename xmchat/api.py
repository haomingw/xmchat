import re
import time

import requests
import pyqrcode

BASE_URL = 'https://login.weixin.qq.com'


class WechatAPI:
    def __init__(self):
        self.session = requests.Session()

    def request(self, url: str, method='GET', status_code=200, **kwargs):
        return self.session.request(url=url, method=method, **kwargs)

    def get_uuid(self) -> str:
        url = BASE_URL + '/jslogin'
        params = {
            'appid': 'wx782c26e4c19acffb',
            'fun': 'new',
            'lang': 'zh_CN',
            '_': int(time.time()),
        }
        response = self.request(url, method='POST', params=params)
        print(response.text)
        pattern = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
        result = re.search(pattern, response.text)
        return result.group(2)

    def gen_qrcode(self, path: str):
        uuid = self.get_uuid()
        url = BASE_URL + f'/l/{uuid}'
        code = pyqrcode.create(url)
        code.png(path, scale=5)
