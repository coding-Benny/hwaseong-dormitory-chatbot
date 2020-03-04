import json
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route("/meal", methods=['POST'])

def getDateInfo():
    req = request.get_json()
    userInputDay = req["action"]["detailParams"]["sys_date"]["origin"]
    requestedDateInfo = req["action"]["params"]["sys_date"]
    requestedDateObj = json.loads(requestedDateInfo)
    requestedDate = requestedDateObj.get("date")
    requestedDateList = requestedDate.split("-")
    year = requestedDateList[0]
    month = requestedDateList[1]
    date = requestedDateList[2]
    dateMessage = userInputDay + "(" + requestedDate + ")"

    mealInfoURL = requests.get('http://www.hstree.org/admin_hs/main/z1_food1.php?gmglory=1&page_no=34&years=' + year + '&months=' + month + '&days=' + date)
    soup = BeautifulSoup(mealInfoURL.content, 'html.parser')
    diets = soup.select("td")
    dobong = 1

    breakfast = diets[switch(userInputDay)].get_text()
    lunch = diets[switch(userInputDay)+7].get_text()
    dinner = diets[switch(userInputDay)+14].get_text()
    breakfast_list = breakfast.split("2관")
    lunch_list = lunch.split("2관")
    dinner_list = dinner.split("2관")
    if breakfast_list[dobong] == '':
        breakfast_list[dobong] = "식단 정보가 없습니다."
    if lunch_list[dobong] == '':
        lunch_list[dobong] = "식단 정보가 없습니다."
    if dinner_list[dobong] == '':
        dinner_list[dobong] = "식단 정보가 없습니다."

    meal = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": userInputDay + "(" + requestedDate + ")" + "\n====== 아침 ======\n" + breakfast_list[dobong] + "\n====== 점심 ======\n" + lunch_list[dobong] + "\n====== 저녁 ======\n" + dinner_list[dobong]
                        }
                    }
                ]
            }
        }
    return jsonify(meal)

def switch(userInputDay):
    return {
        "일요일": 1,
        "월요일": 2,
        "화요일": 3,
        "수요일": 4,
        "목요일": 5,
        "금요일": 6,
        "토요일": 7
    }.get(userInputDay, -1)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

