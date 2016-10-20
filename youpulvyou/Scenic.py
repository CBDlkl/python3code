# coding=utf-8

import urllib
import json
import pymysql
import time

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

youpulvxing1 = "http://m.api.youpu.cn/ypsearch/searchPoi?cityid=%d&model=interestList&package=i2&page=%d&paramType=get&poitype=10&sign=f4a9edcd02e0d2369f0c45ab126b0ac3&timestamp=1474941354"


def GET(url):
    opener = urllib.request.Request(url, headers=send_headers)
    res = urllib.request.urlopen(opener)
    return res.read().decode("utf8")


def Do(begin, end):
    for startIndex in range(begin, end):
        pageIndex = 1
        try:
            html = GET(youpulvxing1 % (startIndex, pageIndex))
            jsonInfo = json.loads(html)

            targeList = jsonInfo['data']['list']

            for i in range(len(targeList)):
                scenicList = {
                    "CityId": (" ", targeList[i]['cityId'])[targeList[i]['cityId'] != ""],
                    "ScenicName": (" ", targeList[i]['cnName'])[targeList[i]['cnName'] != ""],
                    "Describes": (" ", targeList[i]['desc'])[targeList[i]['desc'] != ""],
                    "CityCnName": (" ", targeList[i]['cityCnName'])[targeList[i]['cityCnName'] != ""],
                    "EnName": (" ", targeList[i]['enName'])[targeList[i]['enName'] != ""],
                    "TagName": json.dumps(targeList[i]['tagName'], ensure_ascii=False),
                    "reminder": (" ", targeList[i]["reminder"])[targeList[i]["reminder"] != ""],
                    "Lng": (" ", targeList[i]["lng"])[targeList[i]["lng"] != ""],
                    "Lat": (" ", targeList[i]["lat"])[targeList[i]["lat"] != ""],
                    "PicPath": (" ", targeList[i]["picPath"])[targeList[i]["picPath"] != ""],
                    "JsonData": json.dumps(targeList[i], ensure_ascii=False)
                }
                print("检索到景点: ", scenicList["CityId"], scenicList["ScenicName"], scenicList["CityCnName"],
                      scenicList["Describes"])
                Insert(scenicList)
            ++pageIndex
        except Exception as e:
            print("没有这个数据", e)


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

        sql = "select * from d_city WHERE cityname=%s"
        count = cur.execute(sql, lists["CityCnName"])

        if count < 1:
            print(lists["CityCnName"], ",该城市不存在!")
        else:
            cityid = cur.fetchone()
            print(lists["CityCnName"], "的城市编号:", cityid[0])
            time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            cur.execute(
                " insert into j_viewspot(name, englishname, cityid, playtime, lat, lng, intro, subject, youpujson, createtime) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
                (lists["ScenicName"], lists["EnName"], cityid[0], lists["reminder"], lists["Lat"], lists["Lng"],
                 lists["Describes"], lists["TagName"], lists["JsonData"], time_now))
            cur.execute("SELECT LAST_INSERT_ID()")
            viewspotid = cur.fetchone()[0]

            cur.execute("insert into j_viewspot_img(viewspotid, path, createtime) VALUES (%s,%s,%s)",
                        (viewspotid, lists["PicPath"], time_now))

    except pymysql.Error as e:
        print(e)
    cur.close()
    conn.commit()
    conn.close()


Do(0, 100000)
