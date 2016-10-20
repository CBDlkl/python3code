import urllib.request
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

youpu_city = "http://m.api.youpu.cn/Customline/getCustomCityListByCountryId?countryid=%s&package=i2&paramType=get&sign=32528dc430ca91b2d6f5dd6253509189&timestamp=1475027780"


def GET(url):
    opener = urllib.request.Request(url, headers=send_headers)
    res = urllib.request.urlopen(opener)
    return res.read().decode("utf8")


def Do():
    print("准备执行!")
    try:
        countryids = Query()
        for row in countryids:
            for countryId in row:
                html = GET(youpu_city % countryId)
                jsonInfo = json.loads(html)
                targeList = jsonInfo['data']['cities']
                for index in range(len(targeList)):
                    cityinfo = targeList[index]
                    lists = {
                        "CityId": cityinfo["id"],
                        "CountryId": cityinfo["countryId"],
                        "CityName": cityinfo["name"],
                        "EnName": cityinfo["enName"],
                        "Lat": cityinfo["lat"],
                        "Lng": cityinfo["lng"],
                        "Pic": cityinfo["pic"],
                        "Describes": cityinfo["desc"],
                        "JsonData": json.dumps(cityinfo, ensure_ascii=False)
                    }
                    print(lists["CityId"], lists["CountryId"], lists["Pic"], lists["CityName"], lists["EnName"], lists[
                        "Describes"], lists["Lat"], lists["Lng"])
                    Insert(lists)
    except Exception as e:
        print("没有这个数据", e)


def Query():
    conn = pymysql.connect(
        host="172.16.5.15",
        port=3306,
        user="zhang",
        passwd="zhang",
        db="TravelDataCapture",
        charset="utf8"
    )
    cur = conn.cursor()

    try:
        lists = cur.execute(" select CountryId from YouPu_Country ")
        infos = cur.fetchmany(lists)

    except pymysql.Error as e:
        print(e)
    cur.close()
    conn.commit()
    conn.close()
    return infos


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
        print(lists["CityName"])

        sql = "select * from d_city WHERE cityname=%s "
        count = cur.execute(sql, lists["CityName"])

        if count < 1:
            print(lists["CityName"], ",该城市不存在!")
        else:
            cur.execute(" UPDATE d_city SET youpuid=%s,youpujson=%s WHERE cityname=%s ",
                        (lists["CityId"], lists["JsonData"], lists["CityName"]))

    except pymysql.Error as e:
        print(e)
    cur.close()
    conn.commit()
    conn.close()


Do()
