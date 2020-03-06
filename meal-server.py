import json
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/meal", methods=['POST'])
def main():
    req = request.get_json() # 요청 내용 가져오기
    userInput = req["action"]["detailParams"]["sys_date"]["origin"] # 사용자 입력 내용
    requestedDateInfo = req["action"]["params"]["sys_date"] # 요일에 따른 날짜 정보
    requestedDateObj = json.loads(requestedDateInfo)
    requestedDate = requestedDateObj.get("date")
    requestedDateList = requestedDate.split("-")
    year = requestedDateList[0]
    month = requestedDateList[1]
    date = requestedDateList[2]
    requestedDay = datetime.date(int(year), int(month), int(date))
    requestedDay = requestedDay.strftime("%A") # 날짜에 따른 요일 정보(영어)
    dayDict = {"Sunday": "일요일", "Monday": "월요일", "Tuesday": "화요일", "Wednesday": "수요일", "Thursday": "목요일", "Friday": "금요일", "Saturday": "토요일"}
    requestedDayKor = dayDict.get(requestedDay) # 날짜에 따른 요일 정보(한글)
    f = open('../database/%s.txt' % requestedDate, 'w')

    dateMessage = requestedDayKor + "(" + requestedDate + ")" # 일요일(2020-03-08)

    mealInfoURL = requests.get('http://www.hstree.org/admin_hs/main/z1_food1.php?gmglory=1&page_no=34&years=' + year + '&months=' + month + '&days=' + date)
    soup = BeautifulSoup(mealInfoURL.content, 'html.parser')
    diets = soup.select("td")

    dobong = 1 # 도봉나래관
    errorMessage = "등록된 식단 정보가 없습니다."

    meal = {
        "breakfast": diets[switch(requestedDay)].get_text().split("2관")[dobong],
        "lunch": diets[switch(requestedDay)+7].get_text().split("2관")[dobong],
        "dinner": diets[switch(requestedDay)+14].get_text().split("2관")[dobong],
    }

    if meal["breakfast"] == "":
        meal["breakfast"] = errorMessage
    if meal["lunch"] == "":
        meal["lunch"] = errorMessage
    if meal["dinner"] == "":
        meal["dinner"] = errorMessage

    mealStr = json.dumps(meal, ensure_ascii=False, indent=4)
    f.write(mealStr)
    f.close()

    with open('../database/%s.txt' % requestedDate) as json_file:
        print("get data from file!!")
        json_data = json.load(json_file)
        breakfast = json_data["breakfast"]
        lunch = json_data["lunch"]
        dinner = json_data["dinner"]

    mealMessage = "\n====== 아침 ======\n" + breakfast + "\n====== 점심 ======\n" + lunch + "\n====== 저녁 ======\n" + dinner

    response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": dateMessage + mealMessage
                        }
                    }
                ],
            }
    }
    return jsonify(response)

def switch(requestedDay):
    return {
        "Sunday": 1,
        "Monday": 2,
        "Tuesday": 3,
        "Wednesday": 4,
        "Thursday": 5,
        "Friday": 6,
        "Saturday": 7
    }.get(requestedDay, -1)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

