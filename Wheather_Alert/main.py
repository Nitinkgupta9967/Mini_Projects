import json
import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://api.openweathermap.org/data/2.5/forecast"
parameters = {
    "lat": 19.185932,
    "lon": 72.860054,
    "appid": os.getenv("OPENWEATHER_API_KEY"),
    "cnt": 4
}

response = requests.get(url, params=parameters)
response.raise_for_status()
response_in_json = response.json()

with open("weather.txt", "w") as file:
    json.dump(response_in_json, file, indent=4)

weather_list = response_in_json["list"]
ids = [item["weather"][0]["id"] for item in weather_list]

rainy = any(id < 700 for id in ids)

if rainy:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Hello there, It's Likely To Rain Today Don't Forgot to Take Umbrella",
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to=os.getenv("USER_PHONE_NUMBER")
    )

    print(message.body)
else:
    print("No sign of rain today, have a nice day!!")

print("Weather condition codes:", ids)