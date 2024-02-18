from supabase import create_client, Client
# pip install supabase


class SupaDatabase:
    def __init__(self):
        self.data_values = None
        self.response = None
        url = "https://qimsvuhqcyinjgkyesxm.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFpbXN2dWhxY3lpbmpna3llc3htIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUyMjcxODcsImV4cCI6MjAyMDgwMzE4N30.q3PkL8ix_0l-YSg9PhX0_lek9LkxEvGO6k6xVTI_Pw0"
        self.supabase: Client = create_client(url, key)

    def supabase_data_get(self):
        self.response = self.supabase.table('SensorOut').select("WaterOut, WaterIn, LedStatus").execute()
        self.data_values = dict(self.response)
        return self.data_values["data"]

    def supabase_data_send(self, WaterOut: int = 0, LedStatus: int = 0, WaterIn: int = 0):
        data, count = self.supabase.table('SensorOut').insert(
            {"WaterOut": WaterOut,
             "WaterIn": WaterIn,
             "LedStatus": LedStatus}).execute()

    def real_time_data(self):
        self.response = self.supabase.table('RealData').select("Temperature, Pressure, Moisture, Humidity").execute()
        self.data_values = dict(self.response)
        return self.data_values["data"]

    def rain_data(self):
        self.response = self.supabase.table('RainPP').select("Rain").execute()
        self.data_values = dict(self.response)
        return self.data_values["data"]

    def sensor_data(self):
        self.response = self.supabase.table('sensordata').select(
            "Date, Temperature, Pressure, Moisture, Humidity").execute()
        self.data_values = dict(self.response)
        return self.data_values["data"]

    def sensorout_update(self, name: str, value1: int):
        data, count = self.supabase.table('SensorOut').update({name: value1}).eq('id', 1).execute()

    def mode_check(self):
        response = self.supabase.table("Mode").select('Mode').execute()
        data = dict(response)
        return data["data"]

    def mode_change(self, value2):
        data, count = self.supabase.table('Mode').update({'Mode': value2}).eq('id', 1).execute()
