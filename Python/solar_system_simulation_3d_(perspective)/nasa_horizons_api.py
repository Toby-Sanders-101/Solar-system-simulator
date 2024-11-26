import requests
import datetime
import constants as const

planets = const.planets

#date = "2024-08-17"
#url = f"https://ssd.jpl.nasa.gov/api/horizons.api?format=text&EPHEM_TYPE='VECTORS'&TLIST=\
#    '{date}'&VEC_TABLE='2'&RANGE_UNITS=KM&COMMAND="
#url.replace("'", "%27")

def get_file_at(date, planet, planet_code):
    #print(date, planet, planet_code)
    url = f"https://ssd.jpl.nasa.gov/api/horizons.api?format=text&EPHEM_TYPE='VECTORS'&TLIST=\
        '{date}'&VEC_TABLE='2'&RANGE_UNITS=KM&COMMAND="
    url.replace("'", "%27")
    response = requests.get(url+planet_code)
    if response.status_code == 200:
        f = open(const.base_path + f"nasa_horizons_data/{planet}_{date}.txt","w")
        f.write(response.text)
        f.close()
    else:
        print(f"request for {planet} failed with code {response.status_code}...\nresponse=\n{response.text}")

def get_file_today(planet, planet_code):
    date = datetime.datetime.now().strftime(r"%Y-%m-%d")
    get_file_at(date, planet, planet_code)

def get_all_at(date):
    #print(date)
    url = f"https://ssd.jpl.nasa.gov/api/horizons.api?format=text&EPHEM_TYPE='VECTORS'&TLIST=\
        '{date}'&VEC_TABLE='2'&RANGE_UNITS=KM&COMMAND="
    url.replace("'", "%27")

    for key, value in planets.items():
        response = requests.get(url+value)

        if response.status_code == 200:
            f = open(const.base_path + f"nasa_horizons_data/{key}_{date}.txt","w")
            f.write(response.text)
            f.close()
        else:
            print(f"request for {key} failed with code {response.status_code}...\nresponse=\n{response.text}")

def get_all_today():
    date = datetime.datetime.now().strftime(r"%Y-%m-%d")
    get_all_at(date)
