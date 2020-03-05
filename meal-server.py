import json
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/meal", methods=['POST'])
def main():
    f = open("meal.txt", 'w')
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
    requestedDay = requestedDay.strftime("%A") # 날짜에 따른 요일 정보
    dayDict = {"Sunday": "일요일", "Monday": "월요일", "Tuesday": "화요일", "Wednesday": "수요일", "Thursday": "목요일", "Friday": "금요일", "Saturday": "토요일"}
    requestedDayKor = dayDict.get(requestedDay)
    dateMessage = requestedDayKor + "(" + requestedDate + ")" # 일요일(2020-03-08)

    mealInfoURL = requests.get('http://www.hstree.org/admin_hs/main/z1_food1.php?gmglory=1&page_no=34&years=' + year + '&months=' + month + '&days=' + date)
    soup = BeautifulSoup(mealInfoURL.content, 'html.parser')
    diets = soup.select("td")

    dobong = 1 # 도봉나래관
    errorMessage = "등록된 식단 정보가 없습니다."

    try:
        meal = { # 일주일치 식단 정보
            "Sunday": {
                "breakfast": diets[1].get_text().split("2관")[dobong],
                "lunch": diets[8].get_text().split("2관")[dobong],
                "dinner": diets[15].get_text().split("2관")[dobong],
            },
            "Monday": {
                "breakfast": diets[2].get_text().split("2관")[dobong],
                "lunch": diets[9].get_text().split("2관")[dobong],
                "dinner": diets[16].get_text().split("2관")[dobong],
            },
            "Tuesday": {
                "breakfast": diets[3].get_text().split("2관")[dobong],
                "lunch": diets[10].get_text().split("2관")[dobong],
                "dinner": diets[17].get_text().split("2관")[dobong],
            },
            "Wednesday": {
                "breakfast": diets[4].get_text().split("2관")[dobong],
                "lunch": diets[11].get_text().split("2관")[dobong],
                "dinner": diets[18].get_text().split("2관")[dobong],
            },
            "Thursday": {
                "breakfast": diets[5].get_text().split("2관")[dobong],
                "lunch": diets[12].get_text().split("2관")[dobong],
                "dinner": diets[19].get_text().split("2관")[dobong],
            },
            "Friday": {
                "breakfast": diets[6].get_text().split("2관")[dobong],
                "lunch": diets[13].get_text().split("2관")[dobong],
                "dinner": diets[20].get_text().split("2관")[dobong],
            },
            "Saturday": {
                "breakfast": diets[7].get_text().split("2관")[dobong],
                "lunch": diets[14].get_text().split("2관")[dobong],
                "dinner": diets[21].get_text().split("2관")[dobong],
            }
        }
        if meal[requestedDay]["breakfast"] == "":
            meal[requestedDay]["breakfast"] = errorMessage
        if meal[requestedDay]["lunch"] == "":
            meal[requestedDay]["lunch"] = errorMessage
        if meal[requestedDay]["dinner"] == "":
            meal[requestedDay]["dinner"] = errorMessage
    except:
        print("인덱스 초과!!")

    mealStr = json.dumps(meal, ensure_ascii=False, indent=4)
    f.write(mealStr)
    f.close()

    mealMessage = "\n====== 아침 ======\n" + meal[requestedDay]["breakfast"] + "\n====== 점심 ======\n" + meal[requestedDay]["lunch"] + "\n====== 저녁 ======\n" + meal[requestedDay]["dinner"]

    response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": dateMessage + mealMessage
                        }
                    }
                ]
            }
         }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

