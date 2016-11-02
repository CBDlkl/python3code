import urllib.request


def Get(url):
    print(url)
    try:
        response = urllib.request.urlopen(url)
        html = response.read()
        return html.decode("utf8")
    except Exception as ex:
        print(ex)
        return None
