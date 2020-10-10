# -*- codeing = utf-8 -*-
# @Time : 2020/10/9 14:10
# @Author : 铁壮

# 请求网页
import time
from urllib import parse
import requests
import re
import os
# 请求头
headers ={
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.125 Safari/537.36 '
}
url_ = 'https://www.vmgirls.com/13344.html'
response = requests.get(url=url_, headers=headers)
html = response.text
# 获取文件夹名
dir_name = re.findall('<h1 class="post-title h3">(.*?)</h1>', html)
# if not os.path.exists(dir_name):
#     os.mkdir(dir_name)
# 解析网页
urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', html)
# 保存图片
for url in urls:
    # 加一秒延迟
    time.sleep(1)
    # 把相对路径转为绝对路径
    url = parse.urljoin('http://www.vmgirls.com/', url)
    print(url)
    # 文件名
    file_name = url.split('/')[-1]
    response = requests.get(url=url, headers=headers)
    dir_name.append('/')
    print(dir_name)
    # 以二进制形式存储
    with open(dir_name + file_name, mode='wb') as f:
        f.write(response.content)
        print('正在保存', file_name)