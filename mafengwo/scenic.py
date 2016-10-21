import urllib.request
import json
import time
import threading
from mysql import mysqlHelp

threadNum = 10


# 景点列表

def Get(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf8")
    return html


def threadDo(cityids):
    mysql = mysqlHelp.mysql_help()
    for cityid in cityids:
        try:
            time.sleep(0.25)
            url = "http://www.mafengwo.cn/gonglve/sg_ajax.php?sAct=getMapData&iMddid=%s" % cityid[0]
            html = Get(url)
            jsonInfo = json.loads(html)["list"]
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            for scenic in jsonInfo:
                sql = " insert into j_viewspot_mafengwo(name,cityid,rank,source,lat,lng,createtime,mfwjson) values(%s,%s,%s,%s,%s,%s,%s,%s) "

                parameter = (
                    scenic["name"],
                    cityid[1],
                    scenic["rank"],
                    "mafengwo",
                    scenic["lat"],
                    scenic["lng"],
                    time_now,
                    json.dumps(scenic, ensure_ascii=False)
                )

                print('从城市%s导入了景点%s.' % (cityid[0], scenic["name"]), '\n')
                autoid = mysql.InsertOutId(sql, parameter)

                mysql.InsertOrUpdate(
                    " insert into j_viewspot_img_mafengwo(viewspotid,path,createtime) values(%s,%s,%s)",
                    (autoid, scenic["img_link"], time_now))
        except Exception as e:
            print('系统出现一个错误: ', e)


def Go():
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
