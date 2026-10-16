import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import math

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

table = "pscomppars"
columns = ["pl_name", "pl_masse", "disc_telescope", "hostname", "discoverymethod", "disc_year"]
constraints = ["pl_masse between 0.9 and 1.1", "discoverymethod = 'Transit'", "sy_snum = 1"]


# *********** DATA ***********


# star x10, planet x200, distance x.5

def calculate_E(M, e):
    E = M
    for i in range(10):
        E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    return E

a = .5          # AU
e = 0.0167          # eccentricity
P = 365.256         # days

t = 0               # days since perihelion
M = 2 * math.pi * t / P # mean anomally
E = calculate_E(M, e)

x = a * (math.cos(E) - e)
y = a * math.sqrt(1 - e**2) * math.sin(E)

# ****************************


fig, ax = plt.subplots(figsize=(7,7))
ln, = ax.plot([], [], 'o', color='blue')
ax.set_xlim(-.7, .7)
ax.set_ylim(-.7, .7)

AU = 149597870.7 #km     aq                            q                                                                                                    n
pixels_per_AU = ax.transData.transform((1, 0))[0] - ax.transData.transform((0, 0))[0]
earth_diameter_pixels = 2 * (6371 / AU * 200) * pixels_per_AU
earth_markersize = earth_diameter_pixels * 72 / fig.dpi 
ln.set_markersize(earth_markersize)

sun = {"center": (0, 0), "radius": 695700 / AU *10, "color": "#eca53c"}




def init():
    ax.set_xlim(-.7, .7)
    ax.set_ylim(-.7, .7)     
    return ln,

def orbit(frame):
    ax.add_patch(patches.Circle(sun["center"], radius=sun["radius"], color=sun["color"]))
    
    t = frame * 2
    M = 2 * math.pi * t / P
    E = calculate_E(M, e)

    x = a * (math.cos(E) - e)
    y = a * math.sqrt(1 - e**2) * math.sin(E)

    ln.set_data([x], [y])

    return ln,

ani = FuncAnimation(fig, orbit, frames=None, init_func=init, blit=False)
plt.show()