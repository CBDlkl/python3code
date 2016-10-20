# coding=utf-8

import urllib
import json

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

youpu_theme = "http://m.api.youpu.cn/Customline/getCustomTravelTypeList?cityIds=%d&package=i2&paramType=get&showType=sort&sign=ca6195c002cbd0b382959dec9e15335e&timestamp=1475032324"


def GET(url):
    opener = urllib.request.Request(url, headers=send_headers)
    res = urllib.request.urlopen(opener)
    return res.read().decode("utf8")


def Do():
    try:
        countryids = 11  # connect.QueryCityId()
        for row in countryids:
            for cityId in row:
                html = GET(youpu_theme % cityId)
                jsonInfo = json.loads(html)
                targeList = jsonInfo['data'][1]['tags']
                for index in range(len(targeList)):
                    tageinfo = targeList[index]
                    lists = {
                        "ThemeId": tageinfo["id"],
                        "TagName": tageinfo["tagName"],
                        "Pic": tageinfo["pic"],
                        "Uspic": tageinfo["uspic"],
                        "JsonData": json.dumps(tageinfo, ensure_ascii=False)
                    }
                    print("城市ID:" + str(cityId), lists["ThemeId"], lists["TagName"])
    except Exception as e:
        print("发生异常:", e)


Do()
