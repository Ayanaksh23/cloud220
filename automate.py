import requests as r
import schedule
from sendemail import sendfinalmail, sendmail_cyber24
from datetime import datetime


def dateandtime():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.date()


def mod_check():
    mode_req2 = r.get("https://gsac.ac.bd/ap/json/mode.php")
    mode_ch_value2 = int(mode_req2.text)
    return mode_ch_value2


def real_time_data():
    url = 'https://gsac.ac.bd/ap/json/viewW.php'
    response = r.get(url)
    if response.status_code == 200:
        data = response.json()
        return data


def status_check():
    waterin = r.get("https://gsac.ac.bd/ap/json/waterin.php")
    dataWI = waterin.text
    if dataWI == "1":
        print("Water in pump is on.")
    else:
        print("Water in pump is off.")

    waterout = r.get("https://gsac.ac.bd/ap/json/waterout.php")
    dataWO = waterout.text
    if dataWO == 1:
        print("Water Out pump is on.")
    else:
        print("Water Out pump is off.")


def sendsms():
    data = real_time_data2()

    temp_value = data[0]["temp_value"]
    moios_value = data[0]["moisture_value"]
    humidity_value = data[0]["humidity_value"]
    pressure_value = data[0]["pressure_value"]
    rain_value = data[0]["rain_status"]
    rain = "Not Raining"

    if int(rain_value) == 1:
        rain = "Raning Now."
    else:
        rain = "Not Raining"

    apiSecret = "API-KEY"
    deviceId = "DEVICE-Id"
    phone = '+88**********'
    message = f"'Hello This is project AgriFlow'\n\nTemperature: {temp_value}\nHumidity: {humidity_value}\nPressure: {pressure_value}\nRain: {rain_value}\nMoisture: {moios_value}"

    message = {
        "secret": apiSecret,
        "mode": "devices",
        "device": deviceId,
        "sim": 1,
        "priority": 1,
        "phone": phone,
        "message": message
    }

    re = r.post(url="https://www.cloud.smschef.com/api/send/sms", params=message)

    # do something with response object
    result = re.json()

    print(result)


def pump_auto_control():
    data = real_time_data()
    mois = int(data[0]["moisture_value"])
    print(f"Moisture : {mois}")
    rain = int(data[0]["rain_status"])
    if rain == 1:
        rain_status = "It's Raining Now"
        # sendsms()
    else:
        rain_status = "Not Raining."

    if int(mois) <= 20:
        print("Moisture is less than 20%")
        r.get("https://gsac.ac.bd/ap/waterin.php?wi=1")
        print("Turning Pump on.")
    elif int(mois) >= 70:
        r.get("https://gsac.ac.bd/ap/waterin.php?wi=0")
        print("Turning Pump off.")
    if int(mois) >= 75:
        r.get("https://gsac.ac.bd/ap/waterout.php?wo=1")
        print("Turning Water Out Pump On.")
    elif int(mois) <= 70:
        r.get("https://gsac.ac.bd/ap/waterout.php?wo=0")
        print("Turning Water Out Pump Off.")


def real_time_data2():
    url = 'https://gsac.ac.bd/ap/json/viewW.php'
    response = r.get(url)
    if response.status_code == 200:
        data = response.json()
        return data


def sendmail():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.date()
    data = real_time_data2()

    temp_value = data[0]["temp_value"]
    moios_value = data[0]["moisture_value"]
    humidity_value = data[0]["humidity_value"]
    pressure_value = data[0]["pressure_value"]
    rain_value = data[0]["rain_status"]
    rain = "Not Raining"

    if int(rain_value) == 1:
        rain = "Raning Now."
    else:
        rain = "Not Raining"

    try:
        sendmail_cyber24(moios_value, temp_value, humidity_value, now.strftime('%A, %B %d, %Y'),
                         now.strftime('%I:%M:%S %p'), rain, pressure_value)
    except:
        sendfinalmail(moios_value, temp_value, humidity_value, now.strftime('%A, %B %d, %Y %I:%M:%S %p'))


def is_daytime():
    current_hour = datetime.now().hour
    return 6 <= current_hour < 18


def led_automate():
    if is_daytime():
        print("It's daytime.")
        r.get("https://gsac.ac.bd/ap/led.php?le=0")
    else:
        print("It's nighttime.")
        print("Led is Turn On.")
        r.get("https://gsac.ac.bd/ap/led.php?le=1")


# schedule.every(4).seconds.do(status_check)
# schedule.every(2).seconds.do(pump_auto_control)
# schedule.every(30).minutes.do(sendmail)

while True:
    a = mod_check()
    if a == 0:
        schedule.every(4).seconds.do(status_check)
        schedule.every(2).seconds.do(pump_auto_control)
        schedule.every(30).minutes.do(led_automate)
        # schedule.every(30).minutes.do(sendmail)
        schedule.run_pending()
    else:
        print("Project is Manual Mode.")
