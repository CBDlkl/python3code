import urllib.request
import json
from mysql import mysqlHelp
from bs4 import BeautifulSoup

apiUrl = 'http://www.mafengwo.cn/poi/%s.html'

mysql = mysqlHelp.mysql_help()


def do():
    jsonLists = mysql.GetAll(
        " select viewspotid,mfwjson from j_viewspot where source='mafengwo' and mfwdetailjson is null ", ())
    for scenicJson in jsonLists:
        # 数据原型字典
        paramInfo = {
            '描述': '',
            '电话': '',
            '网址': '',
            '交通': '',
            '门票': '',
            '开放时间': '',
            '用时参考': '',
            'mfwdetailjson': ''
        }

        try:
            viewspotid = scenicJson[0]
            scencid = json.loads(scenicJson[1])['id']
            print('搜索景点ID:%s' % scencid)

            response = urllib.request.urlopen(apiUrl % (scencid)).read().decode('utf8')
            soup = BeautifulSoup(response, "html.parser")

            intro = soup.select('dl[class=intro]')
            if len(intro) > 0:
                describe = intro[0].select('dt')
                if len(describe) > 0:
                    paramInfo['描述'] = intro[0].find('dt').get_text()
                for targe in intro[0].select('dd'):
                    paramInfo[targe.find('span').get_text()] = targe.find('p').get_text()
                paramInfo["mfwdetailjson"] = json.dumps(paramInfo, ensure_ascii=False)

                print(paramInfo)
                mysql.InsertOrUpdate(
                    ' update j_viewspot set intro=%s,openingtime=%s,playtime=%s,mfwdetailjson=%s where viewspotid=%s ',
                    (
                        paramInfo['描述'],
                        paramInfo['开放时间'],
                        paramInfo['用时参考'],
                        paramInfo['mfwdetailjson'],
                        viewspotid
                    ))

            else:
                print('id %s 不是景点.' % scencid)
                mysql.InsertOrUpdate(
                    ' update j_viewspot set mfwdetailjson=%s where viewspotid=%s ',
                    (
                        '{}',
                        viewspotid
                    ))
        except  Exception as e:
            print('出现一次错误，%s' % e)


do()
