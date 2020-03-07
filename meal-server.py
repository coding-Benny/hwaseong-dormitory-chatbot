import json
import time
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/meal", methods=['POST'])

def main():
    req = request.get_json() # 요청 내용 가져오기
    requested_date_info = req["action"]["params"]["sys_date"] # 요일에 따른 날짜 정보
    requested_date_obj = json.loads(requested_date_info)
    requested_date = requested_date_obj.get("date")
    requested_date_list = requested_date.split("-")
    year = requested_date_list[0]
    month = requested_date_list[1]
    date = requested_date_list[2]
    requested_day = datetime.date(int(year), int(month), int(date))
    requested_day = requested_day.strftime("%A") # 날짜에 따른 요일 정보(영어)
    day_dict = {"Sunday": "일요일", "Monday": "월요일", "Tuesday": "화요일", "Wednesday": "수요일", "Thursday": "목요일", "Friday": "금요일", "Saturday": "토요일"}
    requested_day_in_kor = day_dict.get(requested_day)
    date_message = requested_day_in_kor + "(" + requested_date + ")"
    with open('../database/%s.txt' % requested_date) as file:
        content = json.load(file)
        breakfast = content["breakfast"]
        lunch = content["lunch"]
        dinner = content["dinner"]
    meal_message = "\n====== 아침 ======\n" + breakfast + "\n====== 점심 ======\n" + lunch + "\n====== 저녁 ======\n" + dinner
    response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": date_message + meal_message
                        }
                    }
                ]
            }
        }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

