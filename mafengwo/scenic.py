import urllib.request
import json
import time
import threading
from bs4 import BeautifulSoup
from mysql import mysqlHelp

listApiUrl = "http://www.mafengwo.cn/gonglve/sg_ajax.php?sAct=getMapData&iMddid=%s"
detailApiUrl = 'http://www.mafengwo.cn/poi/%s.html'


# 景点和详情 列表

def Get(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf8")
    return html


def threadDo(cityids):
    mysql = mysqlHelp.mysql_help(False)
    for cityid in cityids:
        try:
            url = listApiUrl % cityid[0]
            html = Get(url)
            jsonInfo = json.loads(html)["list"]

            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            index = 1
            for scenic in jsonInfo:
                if index == 20:
                    print('提交一次数据.')
                    index = 1
                    mysql.Close()
                index += 1

                detailInfo = GetDetail(scenic)

                if detailInfo is not None:
                    sql = " insert into j_viewspot_mafengwo (name,cityid,rank,source,lat,lng,createtime,mfwjson,intro,openingtime,playtime,mfwdetailjson,price) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

                    parameter = (
                        scenic["name"],
                        cityid[1],
                        scenic["rank"],
                        "mafengwo",
                        scenic["lat"],
                        scenic["lng"],
                        time_now,
                        json.dumps(scenic, ensure_ascii=False),
                        detailInfo['描述'],
                        detailInfo['开放时间'],
                        detailInfo['用时参考'],
                        detailInfo['mfwdetailjson'],
                        detailInfo['门票']
                    )

                    autoid = mysql.InsertOutId(sql, parameter)
                    mysql.InsertOrUpdate(
                        " insert into j_viewspot_img_mafengwo(viewspotid,path,createtime) values(%s,%s,%s)",
                        (autoid, scenic["img_link"], time_now))
                    print('从城市%s导入了景点%s.' % (cityid[0], scenic["name"]), '\n')

        except Exception as e:
            print('系统出现一个错误: ', e)

    mysql.Close()
    print('正在提交数据,', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


def GetDetail(scenicJson):
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
        scencid = scenicJson['id']
        response = urllib.request.urlopen(detailApiUrl % (scencid)).read().decode('utf8')
        soup = BeautifulSoup(response, "html.parser")

        intro = soup.select('dl[class=intro]')
        if len(intro) > 0:
            describe = intro[0].select('dt')
            if len(describe) > 0:
                paramInfo['描述'] = intro[0].find('dt').get_text()
            for targe in intro[0].select('dd'):
                paramInfo[targe.find('span').get_text()] = targe.find('p').get_text()
            paramInfo["mfwdetailjson"] = json.dumps(paramInfo, ensure_ascii=False)
        else:
            return None
    except  Exception as e:
        print('出现一次错误，%s' % e)
    return paramInfo


def Go(threadNum=10):
    print("爬虫跑起来!一共开了%s个线程" % threadNum)
    mysql = mysqlHelp.mysql_help()
    cityids = mysql.GetAll(" select mfwid,cityid from d_city where mfwid != 0 ", ())
    cityidLen = len(cityids)
    listspLits = int(cityidLen / threadNum)
    targeList = []
    for index in range(1, threadNum + 1):
        if index < threadNum:
            targeList.append(cityids[listspLits * (index - 1):listspLits * index])
        else:
            targeList.append(cityids[listspLits * (index - 1):])

    for targeData in targeList:
        t = threading.Thread(target=threadDo, args=(targeData,))
        t.setDaemon(True)
        t.start()

    t.join()

    print('全部工作完成,%s' % time.ctime())


Go()
