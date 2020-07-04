import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import json, requests

# Generated URL for zip code 16506 from airnowapi.org with my API key and JSON format
# http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=16506&distance=25&API_KEY=77EC22D3-0EB3-4F7D-A1FF-1A68AE5633CB

# Example JSON output
# [{
#     "DateObserved": "2020-07-03 ",
#     "HourObserved": 16,
#     "LocalTimeZone": "EST",
#     "ReportingArea": "Erie",
#     "StateCode": "PA",
#     "Latitude": 42.1292,
#     "Longitude": -80.0851,
#     "ParameterName": "O3",
#     "AQI": 54,
#     "Category": {"Number": 2, "Name": "Moderate"}
# }, {
#     "DateObserved": "2020-07-03 ",
#     "HourObserved": 16,
#     "LocalTimeZone": "EST",
#     "ReportingArea": "Erie",
#     "StateCode": "PA",
#     "Latitude": 42.1292,
#     "Longitude": -80.0851,
#     "ParameterName": "PM2.5",
#     "AQI": 43,
#     "Category": {"Number": 1, "Name": "Good"}
# }]

root = tk.Tk()
root.title("Contacts DataBase")
root.iconbitmap('images/sync.ico')
root.geometry("600x90")


def zip_lookup():
    try:
        zipcode = zip_entry.get()
        api_request = requests.get(f"http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={zipcode}&distance=25&API_KEY=77EC22D3-0EB3-4F7D-A1FF-1A68AE5633CB")
        api = json.loads(api_request.content)
        for result in api:
            if result['ParameterName'] == 'O3':
                city = result['ReportingArea']
                state = result['StateCode']
                aqi = result['AQI']
                cat_number = result['Category']['Number']
                cat_name = result['Category']['Name']
                break
    except Exception as ex:
        aqi = None
        cat_number = None

    if aqi is None:
        air_quality_str = "Error!"
    else:
        air_quality_str = f'{city}, {state} - Air Quality {aqi}, {cat_name}'

    AIR_QUALITY_CATEGORY_COLORS = {
        None: '#888888',  # grey - Error fetching value
        1: '#00E400',  # green - Good
        2: '#FFFF00',  # yellow - Moderate
        3: '#FF7E00',  # flush-orange - Unhealthy for Sensitive Groups
        4: '#FF0000',  # red - Unhealthy
        5: '#8F3F97',  # vived-violet - Very Unhealthy
        6: '#7E0023',  # paprika - Hazardous
        7: '#565656',  # scorpion - Unavailable
    }
    air_quality_color = AIR_QUALITY_CATEGORY_COLORS[cat_number]

    myLabel = ttk.Label(root, text=air_quality_str, font=("Helvetica", 18), background=air_quality_color)
    myLabel.grid(row=1, column=0, columnspan=2)

    root.configure(background=air_quality_color)


zip_entry = ttk.Entry(root)
zip_entry.grid(row=0, column=0, stick=tk.W + tk.E + tk.N + tk.S)

submit_button = ttk.Button(root, text="Lookup Zipcode", command=zip_lookup)
submit_button.grid(row=0, column=1, stick=tk.W + tk.E + tk.N + tk.S)

root.mainloop()
