import requests
import streamlit as st
import pandas as pd
from webapp_supabase import SupaDatabase

st.set_page_config(
    page_title="Project Agriflow",
    page_icon="🎓",
    layout="centered",
)
st.title("🎓 Project Agriflow")
st.header('Hello, This is Project AgriFlow Web Assistant')
st.subheader("Real Time Weather Data...")


def mode_check():
    mode_req = requests.get("https://gsac.ac.bd/ap/json/mode.php")
    mode_ch_value = int(mode_req.text)
    with st.container(border=True):
        if mode_ch_value == 1:
            st.info("Project is now 'Manual Mode'.")
            modeM = st.button('Automatic mode', key='089455_Manual_mode')

            if modeM:
                requests.get("https://gsac.ac.bd/ap/mode.php?mo=0")
                st.success("Mode Change : Automatic")

        elif mode_ch_value == 0:
            st.info("Project is now 'Automatic Mode'.")
            modeM = st.button('Manual Mode', key='0893_Manual_mode')

            if modeM:
                requests.get("https://gsac.ac.bd/ap/mode.php?mo=1")
                st.success("Mode Change : Manual")

        st.warning("⚠️ Project will be go to Automatic Mode in every 30 Minutes.")
        st.info("Please Select manual mode to control field.")
        return mode_ch_value


def real_time_data():
    url = 'https://gsac.ac.bd/ap/json/viewW.php'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data


def view_real_time_data():
    data = real_time_data()
    pdframe = pd.DataFrame(data,
                           columns=['temp_value', 'moisture_value', 'pressure_value', 'humidity_value', 'ptem_value'])
    column_name_mapping = {
        'id': 'id',
        'temp_value': 'Tempeture',
        'moisture_value': 'Moisture',
        'pressure_value': 'Pressure',
        'humidity_value': 'Humidity',
        'ptem_value': 'ptem'
    }
    pdframe = pdframe.rename(columns=column_name_mapping)
    st.table(pdframe)

    if data[0]['rain_status'] == 1:
        st.info("🌧️ It can be Raining today.")
    else:
        st.info("☀️ No significant rain expected.")

    with st.container(border=True):
        tem65 = int(data[0]["temp_value"])
        st.slider("Temperature", 0, 100, int(tem65))
        if 10 <= tem65 < 20:
            st.info("Weather is Too cold.")
        elif 20 <= tem65 <= 25:
            st.info("Weather is Cold.")
        elif 25 <= tem65 <= 33:
            st.info("Beautiful Weather.")
        elif 33 <= tem65 <= 40:
            st.info("Weather is Hot.")
        else:
            st.info("Weather is Too Hot.")

    with st.container(border=True):
        mos65 = data[0]["moisture_value"]
        st.slider("Moisture", 0, 100, int(mos65))

    with st.container(border=True):
        hum65 = int(data[0]["humidity_value"])
        st.slider("Humidity", 0, 100, int(hum65))

    with st.container(border=True):
        pre65 = int(data[0]["pressure_value"])
        st.slider("Pressure", 0, 200000, int(pre65))


data_refresh = st.button("Refresh Data", key="783hjfhdj")
if data_refresh:
    real_time_data()


class PumpStatus:
    def __init__(self):
        self.waterin_url = "https://gsac.ac.bd/ap/json/waterin.php"
        self.waterout_url = "https://gsac.ac.bd/ap/json/waterout.php"
        self.led_url = "https://gsac.ac.bd/ap/json/led.php"

    def waterin_status(self):
        response1 = requests.get(self.waterin_url)
        r1 = int(response1.text)
        # st.info(int(response1.text))
        if r1 == 0:
            st.info("Water In Pump is OFF.")
            pump_on1 = st.button("Turn On Pump", key="010pump")
            if pump_on1:
                requests.get("https://gsac.ac.bd/ap/waterin.php?wi=1")
                st.success("Pump is ON.")
        elif r1 == 1:
            st.info("Water In Pump is ON.")
            pump_off1 = st.button("Turn Off Pump", key="02pump")
            if pump_off1:
                requests.get("https://gsac.ac.bd/ap/waterin.php?wi=0")
                st.success("Pump is OFF.")
        else:
            st.info("Data Error.")

    def led_status(self):
        response3 = requests.get(self.led_url)
        r3 = int(response3.text)

        if r3 == 0:
            st.info("LED is OFF.")
            led_on1 = st.button("Turn On LED", key="010LED")
            if led_on1:
                requests.get("https://gsac.ac.bd/ap/led.php?le=1")
                st.success("LED is ON.")
        elif r3 == 1:
            st.info("LED is ON.")
            led_off1 = st.button("LED Off LED", key="02LED")
            if led_off1:
                requests.get("https://gsac.ac.bd/ap/led.php?le=0")
                st.success("LED is OFF.")
        else:
            st.info("Data Error.")

    def waterout_status(self):
        response2 = requests.get(self.waterout_url)
        # st.info(response2.text)
        r2 = int(response2.text)
        if r2 == 0:
            st.info("Water Out Pump is OFF.")
            pump_on2 = st.button("Turn On Pump", key="03pump")
            if pump_on2:
                requests.get("https://gsac.ac.bd/ap/waterout.php?wo=1")
                st.success("Pump is ON.")
        elif r2 == 1:
            st.info("Water Out Pump is ON.")
            pump_off2 = st.button("Turn Off Pump", key="04pump")
            if pump_off2:
                requests.get("https://gsac.ac.bd/ap/waterout.php?wo=0")
                st.success("Pump is OFF.")
        else:
            st.info("Data Error.")


def pump_control():
    a = PumpStatus()

    with st.container(border=True):
        tab1, tab2, tab3 = st.tabs(["Water In", "Water OUT", "Led"])
        with tab1:
            a.waterin_status()
        with tab2:
            a.waterout_status()
        with tab3:
            a.led_status()


def sensor_status():
    st.header("Sensor Status")
    a2 = SupaDatabase()
    data3 = a2.sensor_data()
    pdframe1 = pd.DataFrame(data3)

    # Create tabs
    Temperature, Pressure, Moisture, Humidity = st.tabs(["Temperature", "Pressure", "Moisture", "Humidity"])

    # Content for each tab
    with Temperature:
        st.write("Temperature Status: ")
        temframe = pdframe1[["Date", "Temperature"]]
        st.dataframe(temframe)
        tem1 = pdframe1["Temperature"]
        st.bar_chart(tem1)

    with Pressure:
        st.write("Pressure Status: ")
        temframe = pdframe1[["Date", "Pressure"]]
        st.dataframe(temframe.set_index("Date"))
        tem1 = pdframe1["Pressure"]
        st.bar_chart(tem1)

    with Moisture:
        st.write("Moisture Status: ")
        temframe = pdframe1[["Date", "Moisture"]]
        st.dataframe(temframe.set_index("Date"))
        tem1 = pdframe1["Moisture"]
        st.bar_chart(tem1)

    with Humidity:
        st.write("Humidity Status: ")
        temframe = pdframe1[["Date", "Humidity"]]
        st.dataframe(temframe.set_index("Date"))
        tem1 = pdframe1["Humidity"]
        st.bar_chart(tem1)

    st.markdown("***")
    command_input = st.text_input("Enter your Command : ")
    if "who are you" in command_input.lower():
        st.info("I am Project Agriflow. I can do multiple task on Agricultural farm.")
    elif "waterin pump on" in command_input.lower():
        st.info("Turning waterin pump on.")
    elif command_input:
        st.info("I am not configured yet.")

    st.info("💡 I am command based model. You can control me by writing command.")


st.markdown("""<html><head>
<style>
div.st-emotion-cache-1inwz65.ew7r33m0 {
display: none;
}
</style>
</head><body><body></html>
""", unsafe_allow_html=True)

with st.container(border=True):
    mode_check()
    view_real_time_data()
    mode_req2 = requests.get("https://gsac.ac.bd/ap/json/mode.php")
    mode_ch_value2 = int(mode_req2.text)
    pump_control()
    sensor_status()
    # mode_check()
    # pump_control()
    # view_real_time_data()
