import json
import threading
import time
from urllib import request
from wantuapp import models


def Get(url):
    print(url)
    try:
        response = request.urlopen(url)
        html = response.read()
        return html.decode("utf8")
    except Exception as ex:
        print(ex)
        return None


def Begin(ints):
    for index in range(ints[0], ints[1]):
        try:
            html = Get("http://www.hitour.cc/app/productDataForMobile/product_id/%s" % index)
            print(html)
            if html is not None:
                jsonInfo = json.loads(html)
                if 'name' in jsonInfo['data']['description']:
                    print(jsonInfo['data']['description']['name'])

                    if 'price' in jsonInfo['data']['show_prices']:
                        price = jsonInfo['data']['show_prices']['price']
                    if 'title' in jsonInfo['data']['show_prices']:
                        price_title = jsonInfo['data']['show_prices']['title']

                    models.session.add(models.WanTuEntity(
                        product_name=jsonInfo['data']['description']['name'],
                        product_id=jsonInfo['data']['product_id'],
                        status=jsonInfo['data']['status'],
                        price=price,
                        price_title=price_title,
                        jsoninfo=json.dumps(jsonInfo)
                    ))
                    models.session.commit()
        except Exception as ex:
            print(ex)

    models.session.close()


def ThreadWork():
    threads = []
    t1 = threading.Thread(target=Begin, args=([1, 4999],))
    threads.append(t1)
    t2 = threading.Thread(target=Begin, args=([5000, 10000],))
    threads.append(t2)

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    print('全部工作完成,%s' % time.ctime())


models.init_db()
Begin([1, 10000])
