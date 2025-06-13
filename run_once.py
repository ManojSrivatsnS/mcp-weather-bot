# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Kxs_sP4kaBEtkpo9qwmlDS_w0Q4eJJQ0
"""

import json
import requests
from datetime import datetime
import pytz

from weatherer import get_weather
from mailerer import send_email
from sheet_handler import connect_to_sheet

#USER_FILE = "users.json"

#def load_users():
#    with open(USER_FILE, "r") as f:
#        return json.load(f)

def load_users():
    sheet = connect_to_sheet()
    data = sheet.get_all_values()
    headers = data[0]
    users = []

    for row in data[1:]:
        user = dict(zip(headers, row))
        users.append({
            "name": user.get("name"),
            "email": user.get("email"),
            "city": user.get("city"),
            "location": user.get("location"),
            "timezone": user.get("timezone")
        })

    return users
def is_near_7am(timezone_str):
    now = datetime.now(pytz.timezone(timezone_str))
    return now.hour == 7 and now.minute <= 5  # e.g., between 7:00 and 7:05 AM
    #return now.hour == 21 and now.minute <= 10  # e.g., between 7:00 and 7:05 AM
    #return True

def run_scheduler_once():
    print("⏰ Running single-pass scheduler...")
    users = load_users()

    for user in users:
        try:
            if is_near_7am(user["timezone"]):
                print(f"📩 Sending weather to {user['email']} ({user['city']})")
                weather = get_weather(user["location"])
                send_email(user["email"], weather, user["city"])
            else:
                print(f"⏳ Skipping {user['email']} — not near 7 AM in {user['timezone']}")
        except Exception as e:
            print(f"❌ Error processing {user['email']}: {e}")

run_scheduler_once()

