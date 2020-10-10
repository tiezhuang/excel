import urllib.request
import re
import csv
import requests
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.121 Safari/537.36 '
}
# user-agent 自己的身份
url_ = "https://z-bgnet.bianguo.com.cn:9101/hzsh/public/api/index/getVote/openid=oci9r5H2YgjWzeh87hOuInWltEFs&keyword=&page=1&pageSize=200"
response = requests.get(url=url_, headers=headers)
html = response.text
print(html)

# host = r'https://z-bgnet.bianguo.com.cn:9101/hzsh/public/api/index/getVote/openid=oci9r5H2YgjWzeh87hOuInWltEFs&keyword=&page=1&pageSize=200'
# r = urllib.request.urlopen(host)
# bs = html.read().decode("utf-8")
pname = r'username":"(.*?)"'
pjob = r'job":"(.*?)"'
phit = r'"hits":(.*?),'
pyxhit = r'"yxhits":(.*?),'
usernames = re.findall(pname, html)
jobs = re.findall(pjob, html)
hits = re.findall(phit, html)
yxhits = re.findall(pyxhit, html)

f = open('投票明细01.csv', 'w', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(["姓名", "职位", "杰出票数", "优秀票数"])
for i in range(0, len(usernames)):
    csv_writer.writerow([usernames[i], jobs[i], hits[i], yxhits[i]])
f.close()
