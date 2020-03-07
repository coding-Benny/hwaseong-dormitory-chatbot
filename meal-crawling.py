import json
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
from flask import request

class Main:
    def main(self):
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

        dateMessage = requestedDayKor + "(" + requestedDate + ")" # 일요일(2020-03-08)

        f = open('%s.txt' % requestedDate, 'w')

        mealInfoURL = requests.get('http://www.hstree.org/admin_hs/main/z1_food1.php?gmglory=1&page_no=34&years=' + year + '&months=' + month + '&days=' + date)
        soup = BeautifulSoup(mealInfoURL.content, 'html.parser')
        diets = soup.select("td")

        dobong = 1 # 도봉나래관
        errorMessage = "등록된 식단 정보가 없습니다."

        meal = {
            "breakfast": diets[switch(requestedDay)].get_text().split("2관")[dobong],
            "lunch": diets[switch(requestedDay)+7].get_text().split("2관")[dobong],
            "dinner": diets[switch(requestedDay)+14].get_text().split("2관")[dobong]
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
        return requestedDate

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
    main()

