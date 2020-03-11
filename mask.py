import requests

mask_open_api = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json?'
latitude = 'lat=37.6445243&'
longitude = 'lng=127.034310&'
meter = 'm=500'

res = requests.get(mask_open_api + latitude + longitude + meter)


if res.status_code == 200:
    data = res.json()
    print(data['stores'][0]['created_at'])
    for store in data['stores']:
        try:
            print(store['name'] + ":" + store['addr'] + "->" + store['remain_stat'] + "|" + store['stock_at'])
        except TypeError:
            store['remain_stat'] = "정보없음"
            store['stock_at'] = "정보없음"
            print(store['name'] + ":" + store['addr'] + "->" + store['remain_stat'] + "|" + store['stock_at'])

