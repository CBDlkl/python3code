# coding=utf-8

import urllib
import json
import pymysql

send_headers = {
    "Host": "m.api.youpu.cn",
    "ypimg": "%7B%0A%20%20%22sPic%22%20:%20%7B%0A%20%20%20%20%22w%22%20:%20%22193%22,%0A%20%20%20%20%22h%22%20:%20%22193%22%0A%20%20%7D,%0A%20%20%22screen%22%20:%20%7B%0A%20%20%20%20%22w%22%20:%20%22640%22,%0A%20%20%20%20%22h%22%20:%20%221136%22%0A%20%20%7D,%0A%20%20%22bPic%22%20:%20%7B%0A%20%20%20%20%22w%22%20:%20%22640%22,%0A%20%20%20%20%22h%22%20:%20%22360%22%0A%20%20%7D%0A%7D",
    "identity": "72F00FDF-94BD-4B86-8D22-9C922A068486",
    "ypmtype": "iPhone 5S",
    "Accept": "*/*",
    "Accept-Language": "zh-Hans-CN;q=1, en-CN;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Version": "3.2.6",
    "User-Agent": "YoupuTrip/3.2.6 (iPhone; iOS 9.0.2; Scale/2.00)"
}

youpulvxing = "http://m.api.youpu.cn/country/getDestList?package=i2&paramType=get&showType=letter&sign=1fa9190e3c354c88ae2947296fb5a08d&timestamp=1475027072"


def GET(url):
    opener = urllib.request.Request(url, headers=send_headers)
    res = urllib.request.urlopen(opener)
    return res.read().decode("utf8")


def Do():
    try:
        html = GET(youpulvxing)
        jsonInfo = json.loads(html)
        targeList = jsonInfo['data']['countryList']
        for i in range(len(targeList)):
            countryLists = targeList[i]['list']
            for j in range(len(countryLists)):
                cnNames = countryLists[j]
                lists = {
                    "id": (" ", cnNames["id"])[cnNames["id"] != ""],
                    "cnName": (" ", cnNames["cnName"])[cnNames["cnName"] != ""],
                    "type": (" ", cnNames["type"])[cnNames["type"] != ""],
                    "pic": (" ", cnNames["pic"])[cnNames["pic"] != ""],
                    "jsonData": json.dumps(cnNames, ensure_ascii=False)
                }
                print(lists["id"], lists["cnName"], lists["type"], lists["pic"])
                Insert(lists)

    except Exception as e:
        print("没有这个数据:", e)


def Insert(lists):
    conn = pymysql.connect(
        host="172.16.5.15",
        port=3306,
        user="zhang",
        passwd="zhang",
        db="fasttrave",
        charset="utf8"
    )
    cur = conn.cursor()

    try:
        cur.execute(" UPDATE d_nation SET youpuid=%s WHERE nationname=%s ",
                    (lists["id"], lists["cnName"]))
    except pymysql.Error as e:
        print(e)
    cur.close()
    conn.commit()
    conn.close()


Do()
