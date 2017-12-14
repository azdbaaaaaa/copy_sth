#!/usr/bin/env python
# -*- coding:UTF-8 -*-

import Cookie
import urllib
import urllib2
import cookielib


c = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(c))
login_path = 'https://passport.lagou.com/login/login.html'
data = {'username': '18717975845', 'password': 'xiaocao732'}
post_info = urllib.urlencode(data)
request = urllib2.Request(login_path, post_info)
html = opener.open(request).read()

if c:
    print c

c.save('cookie.txt')