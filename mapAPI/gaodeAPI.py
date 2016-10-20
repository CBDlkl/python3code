# 路径规划 高德地图API
# API接口地址:http://restapi.amap.com/v3/direction/transit/integrated
# 文档地址:http://lbs.amap.com/api/webservice/guide/api/direction/#bus

import urllib.request
import json
from urllib.parse import urlencode

apiurl = "http://restapi.amap.com/v3/direction/transit/integrated?"
data = {
    'key': 'e5816bfe69aa4a3ec7871aeedea4d14e',
    'origin': '116.551485,39.782881',
    'destination': '109.194819,30.404983',
    'city': '北京',
    'cityd': '恩施'
}

response = urllib.request.urlopen(apiurl + urlencode(data)).read().decode('utf-8')
jsoninfo = json.loads(response)

if int(jsoninfo['count']) > 0:
    route = jsoninfo['route']
    transits = route['transits']
    all_time = 0
    transit_cost = 0
    index = 0
    for transit in transits:
        # 区间预计价格
        transit_cost += float(transit['cost'])
        # 区间预计时间
        all_time += int(transit['duration'])
        index += 1
    print('方案%s: 目标间距离为:%s公里, 预计需要时间:%s 小时, 大约需要花费:%s元' % (
        index,
        round(int(route['distance']) / 1000, 2),
        round(int(all_time) / 60 / 60, 2),
        round(transit_cost, 2)
    ))
