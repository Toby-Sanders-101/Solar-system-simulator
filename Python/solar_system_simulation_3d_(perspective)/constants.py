import math
import pathlib

G = 6.67428e-11
width, height = 800, 800
window_width = 400
trail_length = 100
log10_init_dt = 2.0
init_scroll = -67
scroll_min = -72
scroll_max = -32
scale_min_for_vis_moons = 2**(-56/2)
clicking_uncertainty = 10

font_colour = (255,255,255)
background_colour = (0,0,0)

frame_rate = 24
movement_updates_per_frame = 6 #must be at least 1

base_path = pathlib.Path(__file__).parent.resolve().__str__() + "\\"

real_planets = ["sun", "mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto"]

planets = {"sun": "10",
           "mercury": "199",
           "venus": "299",
           "moon": "301",
           "earth": "399",
           "phobos": "401",
           "deimos": "402",
           "mars": "499",
           "io": "501",
           "europa": "502",
           "ganymede": "503",
           "callisto": "504",
           "amalthea": "505",
           "himalia": "506",
           "thebe": "514",
           "adrastea": "515",
           "metis": "516",
           "jupiter": "599",
           "mimas": "601",
           "enceladus": "602",
           "tethys": "603",
           "dione": "604",
           "rhea": "605",
           "titan": "606",
           "hyperion": "607",
           "iapetus": "608",
           "phoebe": "609",
           "janus": "610",
           "epimetheus": "611",
           "helene": "612",
           "atlas": "615",
           "prometheus": "616",
           "pandora": "617",
           "pan": "618",
           "saturn": "699",
           "ariel": "701",
           "umbriel": "702",
           "titania": "703",
           "oberon": "704",
           "miranda": "705",
           "uranus": "799",
           "triton": "801",
           "naiad": "803",
           "thalassa": "804",
           "despina": "805",
           "galatea": "806",
           "larissa": "807",
           "proteus": "808",
           "neptune": "899",
           "charon": "901",
           "nix": "902",
           "hydra": "903",
           "pluto": "999"
           }

def radius_to_pixels(r, scale):
    px = max(r*scale, 1)
    #math.log10(r) * (scale * 3.4e10)**(1/4) - 3
    return px

def float_to_standard_form(x):
    return str(round(x/(10**int(math.log10(x))),2))+"x10^"+str(int(math.log10(x)))