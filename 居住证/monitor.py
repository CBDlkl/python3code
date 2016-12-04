import time
from urllib import request, parse
from bs4 import BeautifulSoup

url = 'http://apis.baidu.com/kingtto_media/106sms/106sms?mobile=%s&content=%s&tag=2'
key = '****'
tels = '186****9719'


def sendMeg(tel, msg):
    try:
        targeUrl = url % (tel, parse.quote(msg))
        req = request.Request(url=targeUrl, headers={"apikey": key})
        response = request.urlopen(req)
        print(response.read().decode('utf-8'))
    except Exception as ex:
        print(ex)


print("监测服务已开启")

testTime = 0
var = 1
while var == 1:
    testTime += 1
    time.sleep(3)
    if testTime is 40:
        sendMeg('18672959719', '【凯信通】验证码：0000，服务正常。')
    try:
        content = request.urlopen("https://www.bjjzzpt.com/").read().decode('utf-8')
        soup = BeautifulSoup(content)
        if soup.select('.bzyy')[0]['href'] != '###':
            sendMeg(tels, '【凯信通】验证码：0000，居住证办理通道已经开启。')
            break
    except Exception as ex:
        print(ex)

sendMeg(tels, '【凯信通】验证码：0000，服务停止。')
print("工作完成短信已经发送")
