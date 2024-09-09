import requests
import datetime

planets = {"sun": "10",
           "mercury": "199",
           "venus": "299",
           "moon": "301",
           "earth": "399",
           "mars": "499",
           "jupiter": "599",
           "saturn": "699",
           "uranus": "799",
           "neptune": "899"
           }

#date = "2024-08-17"
#url = f"https://ssd.jpl.nasa.gov/api/horizons.api?format=text&EPHEM_TYPE='VECTORS'&TLIST=\
#    '{date}'&VEC_TABLE='2'&RANGE_UNITS=KM&COMMAND="
#url.replace("'", "%27")

def get_all_at(date):
    print(date)
    url = f"https://ssd.jpl.nasa.gov/api/horizons.api?format=text&EPHEM_TYPE='VECTORS'&TLIST=\
        '{date}'&VEC_TABLE='2'&RANGE_UNITS=KM&COMMAND="
    url.replace("'", "%27")

    for key, value in planets.items():
        response = requests.get(url+value)

        if response.status_code == 200:
            f = open(fr"c:\Users\tobyj\Documents\Programming\Visual Studios\solar_system_simulation_2d\nasa_horizons_data\{key}_{date}.txt","w")
            f.write(response.text)
            f.close()
        else:
            print(f"request for {key} failed with code {response.status_code}...\nresponse=\n{response.text}")

def get_all_today():
    date = datetime.datetime.now().strftime(r"%Y-%m-%d")
    get_all_at(date)
