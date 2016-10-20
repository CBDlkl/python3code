import urllib.request
import json
from mysql import mysqlHelp


# 城市列表

def Get(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf8")
    return html


def Do():
    mysql = mysqlHelp.mysql_help()
    nationids = mysql.GetAll(" select mfwid from d_nation where mfwid != 0 ", ())
    for nationid in nationids:
        url = "http://www.mafengwo.cn/gonglve/sg_ajax.php?sAct=getMapData&iMddid=%s" % nationid[0]
        html = Get(url)
        jsonInfo = json.loads(html)["list"]

        for citysingel in jsonInfo:
            sql = " update d_city set mfwid=%s, mfwphoto=%s, mfwjson=%s where cityname=%s "
            parameter = (
                citysingel['id'], citysingel['img_link'], json.dumps(citysingel, ensure_ascii=False),
                citysingel['name'])

            print(parameter, '\n')
            mysql.InsertOrUpdate(sql, parameter)


Do()
