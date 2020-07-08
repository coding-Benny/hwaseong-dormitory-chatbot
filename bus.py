import json
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/bus", methods=['POST'])
def get_bus_info():
    bus = {
        "dir_suyu": {
            "station_id": "109000017",
            "bus_list": {
                "0": {
                   "bus_number": "101",
                    "route_id": "100100006",
                    "order": "14"
                },
                "1": {
                    "bus_number": "106",
                    "route_id": "100100011",
                    "order": "31"
                },
                "2": {
                    "bus_number": "107",
                    "route_id": "100100012",
                    "order": "52"
                },
                "3": {
                    "bus_number": "108",
                    "route_id": "100100013",
                    "order": "75"
                },
                "4": {
                    "bus_number": "130",
                    "route_id": "100100018",
                    "order": "12"
                },
                "5": {
                    "bus_number": "140",
                    "route_id": "100100019",
                    "order": "11"
                },
                "6": {
                    "bus_number": "141",
                    "route_id": "100100020",
                    "order": "12"
                },
                "7": {
                    "bus_number": "142",
                    "route_id": "100100021",
                    "order": "11"
                },
                "8": {
                    "bus_number": "150",
                    "route_id": "100100029",
                    "order": "11"
                },
                "9": {
                    "bus_number": "160",
                    "route_id": "100100033",
                    "order": "11"
                },
                "10": {
                    "bus_number": "N15",
                    "route_id": "100100610",
                    "order": "13"
                },
                "11": {
                    "bus_number": "N16",
                    "route_id": "100100592",
                    "order": "11"
                }
            }
        },
        "dir_ssangmun": {
            "station_id": "109000018",
            "bus_list": {
                "0": {
                    "bus_number": "106",
                    "route_id": "100100011",
                    "order": "65"
                },
                "1": {
                    "bus_number": "107",
                    "route_id": "100100012",
                    "order": "88"
                },
                "2": {
                    "bus_number": "108",
                    "route_id": "100100013",
                    "order": "111"
                },
                "3": {
                    "bus_number": "130",
                    "route_id": "100100018",
                    "order": "74"
                },
                "4": {
                    "bus_number": "140",
                    "route_id": "100100019",
                    "order": "77"
                },
                "5": {
                    "bus_number": "141",
                    "route_id": "100100020",
                    "order": "95"
                },
                "6": {
                    "bus_number": "142",
                    "route_id": "100100021",
                    "order": "96"
                },
                "7": {
                    "bus_number": "150",
                    "route_id": "100100029",
                    "order": "114"
                },
                "8": {
                    "bus_number": "160",
                    "route_id": "100100033",
                    "order": "108"
                },
                "9": {
                    "bus_number": "N15",
                    "route_id": "100100610",
                    "order": "133"
                },
                "10": {
                    "bus_number": "N16",
                    "route_id": "100100592",
                    "order": "121"
                }
            }
        }
    }
    bus_str = json.dumps(bus, indent=4)
    bus_dict = json.loads(bus_str)
    service_key = 'yhlCPwoROADMLNmvDN%2Bgc%2BZeJ%2FwkJOwkbV%2B2MRuvDBhk5JJCkMjnTk0RxPRCU1PrGCQHmblrL%2B%2BKLg6s%2BSz%2Bjw%3D%3D'
    dir_dict = {"수유3동우체국": "dir_suyu", "쌍문역": "dir_ssangmun"}
    congestion = {'0': "데이터없음", '3': "여유", '4': "보통", '5': "혼잡"}
    check_is_last = {'0': "막차아님", '1': "막차"}
    req = request.get_json()
    direction = req['userRequest']['utterance']
    direction = direction.replace("\n", "")
    bus_dir = dir_dict.get(direction)
    station_id = bus_dict[bus_dir]['station_id']

    buses = []
    cards = []

    for i in range(len(bus_dict[bus_dir]['bus_list'])):
        bus_number = bus_dict[bus_dir]['bus_list'][str(i)]['bus_number']
        bus_route_id = bus_dict[bus_dir]['bus_list'][str(i)]['route_id']
        order = bus_dict[bus_dir]['bus_list'][str(i)]['order']
        bus_api = 'http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRoute?ServiceKey=' + service_key + '&stId=' + station_id + '&busRouteId=' + bus_route_id + '&ord=' + order
        res = requests.get(bus_api)
        soup = BeautifulSoup(res.content, 'lxml')
        bus_number = soup.find('rtnm').get_text()
        arrive_info1 = soup.find('arrmsg1').get_text()
        congestion_info1 = soup.find('reride_num1').get_text()
        arrive_info2 = soup.find('arrmsg2').get_text()
        congestion_info2 = soup.find('reride_num2').get_text()
        is_last1 = soup.find('islast1').get_text()
        is_last2 = soup.find('islast2').get_text()

        #if arrive_info1 == "곧 도착":
        #    arrive_soon.append(bus_number)

        if arrive_info1 != "곧 도착" and arrive_info1 != "운행종료" and arrive_info1 != "출발대기":
            temp = re.findall(r'\d+', arrive_info1)
            arrive_info1_list = list(map(str, temp))
            minute = arrive_info1_list[0]
            second = arrive_info1_list[1]
            remain_stops = arrive_info1_list[2]
            if is_last1 == '1':
                arrive_info1 = "[막차🚨] " + minute + "분 " + second + "초(" + remain_stops + "정류장, " + congestion.get(congestion_info1) + ")"
            else:
                arrive_info1 = minute + "분 " + second + "초(" + remain_stops + "정류장, " + congestion.get(congestion_info1) + ")"

        if arrive_info2 != "곧 도착" and arrive_info2 != "운행종료" and arrive_info2 != "출발대기":
            temp = re.findall(r'\d+', arrive_info2)
            arrive_info2_list = list(map(str, temp))
            minute = arrive_info2_list[0]
            second = arrive_info2_list[1]
            remain_stops = arrive_info2_list[2]
            if is_last2 == '1':
                arrive_info2 = "[막차🚨] " + minute + "분 " + second + "초(" + remain_stops + "정류장, " + congestion.get(congestion_info2) + ")\n"
            else:
                arrive_info2 = minute + "분 " + second + "초(" + remain_stops + "정류장, " + congestion.get(congestion_info2) + ")"

        bus_info_message = "🚌 " + bus_number + "(" + direction + " 방면)\n"
        arrive_info_message = "- " + arrive_info1 + "\n- " + arrive_info2 + "\n"
        bus_message = bus_info_message + arrive_info_message
        buses.append(bus_message)

    for j in range(0, len(buses), 2):
        try:
            cards.append(buses[j] + buses[j+1])
        except IndexError:
            cards.append(buses[j])

    bus_response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [
                                {
                                    "description": cards[0]
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
                                }
                            ]
                        }
                    }
                ],
            "quickReplies": [
                {
                    "action": "message",
                    "label": "수유3동우체국",
                    "messageText": "수유3동우체국"
                },
                {
                    "action": "message",
                    "label": "쌍문역",
                    "messageText": "쌍문역"
                },
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
    return jsonify(bus_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3300)

