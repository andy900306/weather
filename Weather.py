# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 14:49:46 2022

@author: GIGABYTE
"""
import json
import requests

def get_data(locationName):

    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWB-39466DA2-60DA-43E2-9C31-AC6B5F744861",
        "locationName": locationName,
    }

    response = requests.get(url, params=params)
    print("天氣預報已發送於Line")
    #print(response.status_code)

    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)

        location = data["records"]["location"][0]["locationName"]

        weather_elements = data["records"]["location"][0]["weatherElement"]
        start_time = weather_elements[0]["time"][0]["startTime"]
        end_time = weather_elements[0]["time"][0]["endTime"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]
        return tuple([location, start_time, end_time, weather_state, rain_prob, min_tem, comfort, max_tem])
        # print(location)
        # print(start_time)
        # print(end_time)
        # print(weather_state)
        # print(rain_prob)
        # print(min_tem)
        # print(comfort)
        # print(max_tem)
        
    else:
        print("Can't get data!")
        
        
def line_notify(data):

    token = "IFGHjXdirvDD3OUlBNJNGaS8gflUS2JUc3wLyHXcg7v"
    message = ""

    if len(data) == 0:
        message += "\n[Error] 無法取得天氣資訊"
    else:
        message += f"\n今天{data[0]}的天氣: {data[3]}\n"
        message += f"溫度: {data[5]}°C - {data[7]}°C\n"
        message += f"降雨機率: {data[4]}%\n"
        message += f"舒適度: {data[6]}\n"
        message += f"時間: {data[1]} ~ {data[2]}\n"

        if int(data[4]) > 70:
            message += "提醒您，今天很有可能會下雨，出門記得帶把傘哦!"
        elif int(data[7]) > 33:
            message += "提醒您，今天很熱，外出要小心中暑哦~"
        elif int(data[5]) < 10:
            message += "提醒您，今天很冷，記得穿暖一點再出門哦~"

    # line notify所需資料
    line_url = "https://notify-api.line.me/api/notify"
    line_header = {
        "Authorization": 'Bearer ' + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    line_data = {
        "message": message
    }

    requests.post(url=line_url, headers=line_header, data=line_data)

locationName=["臺中市","彰化縣","臺南市","桃園市"]
for name in locationName:
    data= get_data(name)
    line_notify(data)

