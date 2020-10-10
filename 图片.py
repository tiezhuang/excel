# -*- codeing = utf-8 -*-
# @Time : 2020/10/9 14:54
# @Author : 铁壮
import time
from urllib import parse
import os
import requests
import re

# 请求网页
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.121 Safari/537.36 '
}
# user-agent 自己的身份
url_ = "https://www.vmgirls.com/13344.html"
response = requests.get(url=url_, headers=headers)
html = response.text
# 解析网页
dir_name = re.findall('<h1 class="post-title h1">(.*?)</h1>', html)[-1]
print(dir_name)

urls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', html)
# 判断文件夹dir_name是否存在
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
# 保存图片
for url in urls:
    time.sleep(1)
    # 把绝对路径变成相对路径
    url = parse.urljoin('http://www.vmgirls.com/', url)

    # 图片的名字
    fiel_name = url.split("/")[-1]
    response = requests.get(url, headers=headers)
    print(fiel_name)
    with open(dir_name + '/' + fiel_name, mode='wb') as f:
        f.write(response.content)
