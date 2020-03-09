import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import os
from pytz import timezone

_abs_path = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(filename=f'{_abs_path}/meal.log', format='[%(levelname)s] %(asctime)s | %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S')
logging.debug('Meal Started')

def save_data():
    fmt = "%Y-%m-%d"
    kst = datetime.now(timezone('Asia/Seoul'))
    weekdays = [None]*7
    year = kst.strftime("%Y")
    month = kst.strftime("%m")
    date = kst.strftime("%d")
    meal_info_url = requests.get('http://www.hstree.org/admin_hs/main/z1_food1.php?gmglory=1&page_no=34&years=' + year + '&months=' + month + '&days=' + date)
    soup = BeautifulSoup(meal_info_url.content, 'html.parser')
    diets = soup.select("td")
    dobong = 1 # 도봉나래관
    error_message = "등록된 식단 정보가 없습니다."

    for i in range(0, 7):
        weekdays[i] = kst + timedelta(days=i)
        requested_day = weekdays[i].strftime("%A")
        f = open('/home/ec2-user/api/database/%s.txt' % weekdays[i].strftime(fmt), 'w')
        print(weekdays[i].strftime(fmt))
        meal = {
            "breakfast": diets[switch(requested_day)].get_text().split("2관")[dobong],
            "lunch": diets[switch(requested_day)+7].get_text().split("2관")[dobong],
            "dinner": diets[switch(requested_day)+14].get_text().split("2관")[dobong]
        }

        if meal["breakfast"] == "":
            meal["breakfast"] = error_message
        if meal["lunch"] == "":
            meal["lunch"] = error_message
        if meal["dinner"] == "":
            meal["dinner"] = error_message

        meal_str = json.dumps(meal, ensure_ascii=False, indent=4)
        f.write(meal_str)
        f.close()

def switch(requested_day):
    return {
        "Sunday": 1,
        "Monday": 2,
        "Tuesday": 3,
        "Wednesday": 4,
        "Thursday": 5,
        "Friday": 6,
        "Saturday": 7
    }.get(requested_day, -1)

if __name__ == "__main__":
    save_data()

