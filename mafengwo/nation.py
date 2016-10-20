import urllib.request
from bs4 import BeautifulSoup
from mysql import mysqlHelp


# 国家列表

def Get(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf8")
    return html


def Do():
    url = "http://www.mafengwo.cn/mdd/"
    html = Get(url)
    soup = BeautifulSoup(html)

    items = soup.select("div[data-cs-p='全球目的地'] .bd .item")

    print("目标总数:", len(items))

    mysql = mysqlHelp.mysql_help()

    for item in items:
        continents = item.select(".sub-title")[0].get_text(strip=True)
        print("大洲 => ", continents)

        for singeltext in item.select("a"):
            cityid = singeltext.get("href").replace("/travel-scenic-spot/mafengwo/", "").replace(".html", "")
            citystr = singeltext.get_text().split(' ')
            cityname = citystr[0]
            encityname = citystr[1]

            if cityid == "" or cityname == "":
                continue

            print(cityname, encityname, cityid)

            sql = " update d_nation set mfwid=%s where nationname=%s "
            parameter = (cityid, cityname)

            mysql.InsertOrUpdate(sql, parameter)


Do()
