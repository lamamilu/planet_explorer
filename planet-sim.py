import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import math
from utility import *
import requests

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

table = "pscomppars"
columns = ["pl_name", "pl_masse", "hostname", "pl_orbeccen", "pl_orbper", "pl_orbsmax", "st_rad", "pl_rade"]
constraints = ["pl_name = '16 Cyg B b'"]

query = url + adql(table, columns, constraints)
p = requests.get(query)
print(p.status_code)
p = p.json()[0]
print(p)


# *********** DATA ***********

def calculate_E(M, e):
    E = M
    for i in range(10):
        E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    return E

a = p["pl_orbsmax"]      # AU
e = p["pl_orbeccen"]     # eccentricity
P = p["pl_orbper"]       # days to orbit

t = 0                    # days since perihelion
M = 2 * math.pi * t / P  # mean anomally
E = calculate_E(M, e)

x = a * (math.cos(E) - e)
y = a * math.sqrt(1 - e**2) * math.sin(E)

AU = 149597870.7 #km

# ****************************


def draw_orbit(num_points=1000):
     t = np.linspace(0, P, num_points)

     M = 2 * math.pi * t / P
     E = M
     for i in range(10):
          E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))

     ellipse_x = a * (np.cos(E) - e)
     ellipse_y = a * np.sqrt(1 - e**2) * np.sin(E)
    
     return ellipse_x, ellipse_y

t = 0

ellipse_x, ellipse_y = draw_orbit()


hor = a
ver = a * math.sqrt(1 - e**2)
if hor 
scale = a * (1 + e) * 1.1

fig, ax = plt.subplots(figsize=(10,7))
plt.plot(ellipse_x, ellipse_y, label='Orbit outline', color='green')
ln, = ax.plot([], [], 'o', color='blue')
ax.set_xlim(-(scale), scale)
ax.set_ylim(-(scale), scale)



pixels_per_AU = ax.transData.transform((1, 0))[0] - ax.transData.transform((0, 0))[0]
earth_diameter_pixels = 2 * (p["pl_rade"] / AU * 10) * pixels_per_AU # PLANET SCALE: *10
earth_markersize = earth_diameter_pixels * 72 / fig.dpi 
ln.set_markersize(earth_markersize)

star = {"center": (a*e, 0), "radius": p["st_rad"] * 0.00465} # r in [stellar radius] devided by stellar radius in AU




def init():
    ax.set_xlim(-(scale), scale)
    ax.set_ylim(-(scale), scale)     
    return ln,

def orbit(frame):
    ax.add_patch(patches.Circle(star["center"], radius=star["radius"], color="#eca53c"))
    
    t = frame
    M = 2 * math.pi * t / P
    E = calculate_E(M, e)

    x = a * (math.cos(E) - e)
    y = a * math.sqrt(1 - e**2) * math.sin(E)

    ln.set_data([x], [y])

    return ln,

ani = FuncAnimation(fig, orbit, frames=None, init_func=init, blit=False)
plt.show()