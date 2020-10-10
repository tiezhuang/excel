import urllib.request
import re
import csv

host = r'https://z-bgnet.bianguo.com.cn:9101/hzsh/public/api/index/getVote/openid=oci9r5H2YgjWzeh87hOuInWltEFs&keyword=&page=1&pageSize=200'
r = urllib.request.urlopen(host)
bs = r.read().decode("utf-8")
pname = r'username":"(.*?)"'
pjob = r'job":"(.*?)"'
phit = r'"hits":(.*?),'
pyxhit = r'"yxhits":(.*?),'
usernames = re.findall(pname, bs)
jobs = re.findall(pjob, bs)
hits = re.findall(phit, bs)
yxhits = re.findall(pyxhit, bs)

f = open('投票明细.csv', 'w', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(["姓名", "职位", "杰出票数", "优秀票数"])
for i in range(0, len(usernames)):
    csv_writer.writerow([usernames[i], jobs[i], hits[i], yxhits[i]])
f.close()
