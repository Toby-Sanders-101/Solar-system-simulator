import datetime
import nasa_horizons_api as api
import pathlib

base_path = pathlib.Path(__file__).parent.resolve().__str__()

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

def search_num_beginning(content, string):
    if content.find(string) == -1:
        print(f"could not find {string}")
        return 1
    i = content.find(string) + len(string)
    flag = True
    new_string = ""
    multiplier = 1
    if content[i] == "-":
        multiplier = -1
        i += 1
    while flag:
        if content[i] in "1234567890.":
            new_string += content[i]
        elif content[i] == "~":
            pass
        elif content[i] =="E":
            i += 1
            mag_flag = True
            mag_multiplier = 1
            mag_new_string = ""
            if content[i] == "-":
                mag_multiplier = -1
                i += 1
            elif content[i] == "+":
                i += 1
            while mag_flag:
                if content[i] in "1234567890":
                    mag_new_string += content[i]
                else:
                    mag_flag = False
                i += 1
            mag = mag_multiplier * int(mag_new_string)
            multiplier *= 10 ** mag
            flag = False
        else:
            flag = False
        i += 1
    number = multiplier * float(new_string)
    return number

def read_file(file, planet):
    with open(file, "r") as f:
        content = f.read()
        if "(g)"in content:
            additional = -3
        else:
            additional = 0
        content = content.replace("\t","").replace("\n","").replace(" ","").replace(",","").replace("(g)","kg").replace("(kg)","kg").replace("(km)","km").upper().replace("MASS10^","MASSX10^")
        mass_order_of_magnitude = search_num_beginning(content, "MASSX10^")
        mass = search_num_beginning(content, "MASSX10^"+str(int(mass_order_of_magnitude))+"KG=")
        radius = search_num_beginning(content, "VOL.MEANRADIUSKM=")
        content = content.split("$$SOE")[1]
        x = search_num_beginning(content, "X=") * 1000
        y = search_num_beginning(content, "Y=") * 1000
        z = search_num_beginning(content, "Z=") * 1000
        vx = search_num_beginning(content, "VX=") * 1000
        vy = search_num_beginning(content, "VY=") * 1000
        vz = search_num_beginning(content, "VZ=") * 1000
        return {"m": mass * 10 ** (mass_order_of_magnitude + additional),
                "r": radius,
                "x": x,
                "y": y,
                "z": z,
                "vx": vx,
                "vy": vy,
                "vz": vz,
                "name": planet}

def read_data_from(file, planet, date):
    file = base_path + "/nasa_horizons_data/" + file
    try:
        return read_file(file, planet)
    except:
        print("could not find file...\nattempting to fetch data from nasa...")
        try:
            api.get_all_at(date)
            print("data fetched...\nattempting to find file again...")
            return read_file(file, planet)
        except:
            print("could not fetch data from nasa...\nplease debug...")
            quit()


def read_all_at(date):
    data = []
    for planet in planets.keys():
        file_name = planet+"_"+date+".txt"
        data.append(read_data_from(file_name, planet, date))
    return data

def read_all_today():
    date = datetime.datetime.now().strftime(r"%Y-%m-%d")
    return read_all_at(date)