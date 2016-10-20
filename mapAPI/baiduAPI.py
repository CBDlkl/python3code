# 百度地图API - 路径规划
# API地址:http://api.map.baidu.com/direction/v2/transit
# API文档:http://lbsyun.baidu.com/index.php?title=webapi/direction-api-v2#.E4.BD.BF.E7.94.A8.E6.96.B9.E6.B3.95

# 百度地图API - 地址转经纬度
# API地址:http://api.map.baidu.com/geocoder/v2/
# API文档:http://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding

import urllib.request
import json
import os
from urllib.parse import urlencode

# 开发者ak
ak = 'WOkvM8hfFLrTAZjFZCciXR9L'


# 地理位置名称转经纬度
def AdressNameToLat(name):
    apiurl = 'http://api.map.baidu.com/geocoder/v2/?'
    data = {
        'address': name,
        'output': 'json',
        'ak': ak,
    }

    response = urllib.request.urlopen(apiurl + urlencode(data)).read().decode('utf-8')
    jsoninfo = json.loads(response)
    if int(jsoninfo['status']) == 0:
        location = jsoninfo['result']['location']
        return (location['lat'], location['lng'])


def otherLonLatToBaidu(lonandlat, fromtype=3, totype=5):
    """ google地图坐标、soso地图坐标、amap地图坐标、mapbar地图坐标转换百度坐标系
    lonandlat的参数样例:
        格式：经度,纬度;经度,纬度…
        限制：最多支持100个
        格式举例：
        114.21892734521,29.575429778924;
        114.21892734521,29.575429778924
    fromtype的参数类型:
        1：GPS设备获取的角度坐标，wgs84坐标;
        2：GPS获取的米制坐标、sogou地图所用坐标;
        3：google地图、soso地图、aliyun地图、mapabc地图和amap地图所用坐标，国测局坐标;
        4：3中列表地图坐标对应的米制坐标;
        5：百度地图采用的经纬度坐标;
        6：百度地图采用的米制坐标;
        7：mapbar地图坐标;
        8：51地图坐标
    totype的参数类型:
        5：bd09ll(百度经纬度坐标),
        6：bd09mc(百度米制   经纬度坐标);
    """
    apiurl = 'http://api.map.baidu.com/geoconv/v1/?'
    data = {
        'coords': lonandlat,
        'from': fromtype,
        'to': totype,
        'output': 'json',
        'ak': ak,
    }

    response = urllib.request.urlopen(apiurl + urlencode(data)).read().decode('utf-8')
    jsoninfo = json.loads(response)
    if int(jsoninfo['status']) == 0:
        location = jsoninfo['result']
        return list(location)
    return None


# 路径计算
def CalculationTravelPlan(startname_lonlat, endname_lonlat, is_lonlat=False):
    apiurl = 'http://api.map.baidu.com/direction/v2/transit?'
    origin = startname_lonlat
    destination = endname_lonlat
    if not is_lonlat:
        startLonLat = AdressNameToLat(startname_lonlat)
        origin = '%s,%s' % (startLonLat[0], startLonLat[1])

        endLonLat = AdressNameToLat(endname_lonlat)
        destination = '%s,%s' % (endLonLat[0], endLonLat[1])

    data = {
        'origin': origin,
        'destination': destination,
        'ak': ak,
    }

    response = urllib.request.urlopen(apiurl + urlencode(data)).read().decode('utf-8')
    jsoninfo = json.loads(response)
    result = jsoninfo['result']

    print('从 [%s] 到 [%s] 路线行程共有%s个计划: ' % (
        result['origin']['city_name'],
        result['destination']['city_name'],
        result['total']
    ))

    routes = result['routes']
    index = 1
    for route in routes:
        print('线路规划%s : 距离%s 公里, 大约需要耗时%s 小时.' % (
            index,
            round(int(route['distance']) / 1000, 2),
            round(int(route['duration']) / 60 / 60, 2)
        ))
        index += 1


baiduLatLon = otherLonLatToBaidu('39.9180671069,116.3970073161;39.8350222919,119.4845684844')
# CalculationTravelPlan('北京', '恩施')
CalculationTravelPlan('%s,%s' % (baiduLatLon[0]['x'], baiduLatLon[0]['y']),
                      '%s,%s' % (baiduLatLon[1]['x'], baiduLatLon[1]['y']), True)
