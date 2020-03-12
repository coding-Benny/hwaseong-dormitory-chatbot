import requests
from datetime import datetime
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/mask", methods=['POST'])
def mask():
    mask_open_api = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json?'
    latitude = 'lat=37.6445243&'
    longitude = 'lng=127.034310&'
    meter = 'm=500'

    res = requests.get(mask_open_api + latitude + longitude + meter)

    status_dict = {'break': "🖤", 'empty': "🖤", 'few': "❤", 'some': "💛", 'plenty': "💚"}

    mask_vendors = []
    cards = []

    if res.status_code == 200:
        data = res.json()
        origin_created_at = data['stores'][0]['created_at']
        origin_created_at_object = datetime.strptime(origin_created_at, '%Y/%m/%d %H:%M:%S')
        created_at = origin_created_at_object.strftime('%m/%d %H:%M')
        time_info = "🔎 " + created_at + "\n"

        for i in range(len(data['stores'])):
            try:
                name = data['stores'][i]['name']
                remain_status = status_dict.get(data['stores'][i]['remain_stat'])
                origin_stock_at = data['stores'][i]['stock_at']
                origin_stock_at_object = datetime.strptime(origin_stock_at, '%Y/%m/%d %H:%M:%S')
                stock_at = origin_stock_at_object.strftime('%m/%d %H:%M')
                address = data['stores'][i]['addr'].replace("서울특별시", '')
                mask_message = str(i+1) + ". " + name + remain_status + "\n⏰ : " + stock_at + "\n💊 : " + address + "\n"
                mask_vendors.append(mask_message)

            except TypeError:
                remain_status = "(정보없음)"
                stock_at = "정보없음"
                mask_message = str(i+1) + ". " + name + remain_status + "\n⏰ : " + stock_at + "\n💊 : " + address + "\n"
                mask_vendors.append(mask_message)

        for j in range(0, len(mask_vendors), 2):
            try:
                cards.append(mask_vendors[j] + mask_vendors[j+1])
            except IndexError:
                cards.append(mask_vendors[j])

    mask_response = {
            "version": "2.0",
            "template": {
            "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                    "description": time_info + cards[0]
                                },
                                {
                                    "description": cards[1]
                                },
                                {
                                    "description": cards[2]
                                },
                                {
                                    "description": cards[3]
                                },
                                {
                                    "description": cards[4]
                                },
                                {
                                    "description": cards[5]
                                },
                                {
                                    "description": cards[6]
                                },
                                {
                                    "description": cards[7]
                                },
                                {
                                    "description": cards[8]
                                }
                            ]
                        }
                    }
                ],
            "quickReplies": [
                {
                    "action": "message",
                    "label": "도움말",
                    "messageText": "도움말"
                },
                {
                    "action": "message",
                    "label": "간식이 먹고 싶어요🍪",
                    "messageText": "간식?"
                }
            ]
        }
    }
    return jsonify(mask_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3100)

