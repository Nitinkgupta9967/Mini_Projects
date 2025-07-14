import time
import requests
import smtplib
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

my_lat = 4.0264
my_lng = 121.2175

parameters = {
    "lat" : my_lat,
    "lng" : my_lng,
    "formatted" : 0
}
ss_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
ss_response.raise_for_status()
data1 = ss_response.json()
sunrise = int(data1["results"]["sunrise"].split("T")[1].split(":")[0])
sunset =  int(data1["results"]["sunset"].split("T")[1].split(":")[0])

def check_condition():
    my_email = os.getenv("EMAIL_ADDRESS")
    my_password = os.getenv("EMAIL_PASSWORD")
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_current_lng = float(data["iss_position"]["longitude"])
    iss_current_lat = float(data["iss_position"]["latitude"])
    now = dt.datetime.utcnow()
    hour = now.hour
    print(iss_current_lat,iss_current_lng)
    try:
        if abs(my_lat - iss_current_lat) < 5 and abs(my_lng - iss_current_lng) < 5:
            if hour < sunrise or hour > sunset:
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=my_email,password=my_password)
                    connection.sendmail(from_addr=my_email,to_addrs="nitin.k.gupta@slrtce.in",msg="subject : Reminder To See ISS !!\n\nISS IS JUST ABOVE YOUR HEAD SEE IT NOW")
                    print("Email Sent sucessfully !!")
            else:
                 print("It Is Not Dark Yet !!")
        else:
            print("ISS Is Not Over Your Head !!")
    except Exception as e:
        print(f"An Error Occured {e}")
        print("It Not The Correct Time")

while True:
    time.sleep(60)
    check_condition()