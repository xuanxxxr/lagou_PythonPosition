
import shutil
from http import cookiejar

import requests
import re
import json
import time
import os
import sys


session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename="cookies.txt")

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_dir)
from zheye import zheye

z = zheye()
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4"
}
s = requests.session()
s.cookies = cookiejar.LWPCookieJar(filename="cookies.txt")
response_xsrf = s.get("https://www.zhihu.com", headers=header)
match = re.match('.*name="_xsrf" value="(.*?)"', response_xsrf.text, re.DOTALL)
xsrf = ""
if match:
    xsrf = match.group(1)
random_num = str(int(time.time() * 1000))
response_captcha = s.get("https://www.zhihu.com/captcha.gif?r={}&type=login&lang=cn".format(random_num), headers=header,
                         stream=True)
positions = []
if response_captcha.status_code == 200:
    with open('pic_captcha.gif', 'wb') as f:
        response_captcha.raw.decode_content = True
        shutil.copyfileobj(response_captcha.raw, f)
    positions = z.Recognize('pic_captcha.gif')
    # 解析出来的坐标是y,x要转一些
    # 将坐标按照x从小到大排序
    positions.sort(key=lambda x: x[1])
    positions = [[float(format(i[1] / 2, '0.1f')), float(format(i[0] / 2, '0.1f'))] for i in positions]
    print(positions)
    post_url = "https://www.zhihu.com/login/phone_num"

    params = {
        '_xsrf': xsrf,
        'password': '82120963',
        'captcha': '{0}"img_size": [200, 44], "input_points":{1}{2}'.format('{', positions, '}'),
        'captcha_type': 'cn',
        'phone_num': '17691183665'
    }

    print(params)
    response_login = s.post(post_url, headers=header, params=params)
    s.cookies.save()
    print(response_login.status_code)
    response_text = json.loads(response_login.text)
    print(response_text)

    inbox_url = "https://www.zhihu.com/inbox"
    response = s.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        print("登陆失败")
    else:
        print("登陆成功")

import gc; gc.collect()