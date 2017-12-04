# -*- coding: utf-8 -*-

from zheye import zheye
z = zheye()
positions = z.Recognize('captcha_hanzi.gif')

print(positions)