import requests
from datetime import datetime
import smtplib
import time


MY_LAT = 27.717245
MY_LNG = 85.323959
MY_EMAIL ="shubhamb42069@gmail.com"
password ="pmif sdeb bkgi pzir"
running =True

def is_it():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()["iss_position"]
    iss_longitude = float(data["longitude"])
    iss_latitude = float(data["latitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT + 5 and MY_LNG-5 <= iss_longitude <= MY_LNG + 5:
        print("overhead")
        global running
        running = False
        return True
    else:
        return False

def is_time():
    time_now = datetime.now().hour

    para = { 
        "lat": MY_LAT,
        "lng": MY_LNG,
        "tzid":"Asia/Kathmandu",
        "formatted":0,
    }

    sun = requests.get(url=" https://api.sunrise-sunset.org/json", params = para, )
    sun.raise_for_status()

    hey = sun.json()["results"]

    sunrise = int(hey["sunrise"].split("T")[1].split(":")[0])
    sunset = int(hey["sunset"].split("T")[1].split(":")[0])

    if time_now >= sunset or time_now <= sunrise:
        return True

while running:
    time.sleep(60)
    if is_it() and is_time():
        with smtplib.SMTP("smtp.gmail.com") as connect:
            connect.starttls()
            connect.login(user=MY_EMAIL, password= password)
            connect.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject: Look out for the International Space Station\n\n Hey the space station seems to be passing by you",
            )

         
