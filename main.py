import requests
import datetime as dt
import smtplib
import time

MY_LAT = 43.129178
MY_LONG = -79.213106
running = True


def is_iss_overhead():
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    iss_lng = float(iss_data["iss_position"]["longitude"])
    iss_lat = float(iss_data["iss_position"]["latitude"])

    lat_compare = iss_lat + 5 >= MY_LAT >= iss_lat - 5
    lng_compare = iss_lng + 5 >= MY_LAT >= iss_lng - 5

    in_position = lat_compare and lng_compare

    return in_position


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    time_data = response.json()

    my_time = dt.datetime.now()
    utc_hour = my_time.hour + 5
    if utc_hour > 23:
        utc_hour = 0

    sunrise = int(time_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(time_data["results"]["sunset"].split("T")[1].split(":")[0])

    night = sunset <= utc_hour or utc_hour <= sunrise

    return night


def send_email():
    with smtplib.SMTP("smtp.gmail.com") as email:
        email.starttls()
        email.login(user="paul.jaro@gmail.com", password="N7-koxoness")
        email.sendmail(from_addr="paul.jaro@gmail.com", to_addrs="paulwjaroslawski@gmail.com",
                       msg="Subject: ISS Alert\n\n "
                       "Just letting you know that the International Space Station is flying overhead.")


while running:
    print("Program Searching for ISS")
    if is_iss_overhead() and is_night():
        send_email()
        quit()
    time.sleep(60)
