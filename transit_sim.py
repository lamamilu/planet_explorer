import matplotlib
# matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
import matplotlib.patches as patches
import math
from utility import *
import requests
import ffmpeg

# url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

# table = "pscomppars"
# columns = ["pl_name", "pl_masse", "hostname", "pl_orbeccen", "pl_orbper", "pl_orbsmax", "st_rad", "pl_rade"]
# constraints = ["pl_name = '16 Cyg B b'"] # 16 Cyg B b, Kepler-10 b

# query = url + adql(table, columns, constraints)
# p = requests.get(query)
# print(p.status_code)
# p = p.json()[0]
# print(p)

# *********** DATA ***********

def calculate_E(M, e):
     E = M
     for i in range(10):
          E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
     return E

r = 6371
sr = 695700

a = 1.00      # AU
e = 0.0167     # eccentricity
P = 365.256       # days to orbit

t = 0                    # days since perihelion
M = 2 * math.pi * t / P  # mean anomally
E = calculate_E(M, e)

x = a * (math.cos(E) - e)
y = a * math.sqrt(1 - e**2) * math.sin(E)

AU = 149597870.7 #km

# ****************************

width = 7
height = 7

scale = sr * 1.2

fig, ax = plt.subplots(figsize=(width, height))
ln, = ax.plot([], [], 'o', color='blue')
ax.set_xlim(-(scale), scale) 
ax.set_ylim(-(scale), scale)
ax.set_aspect("equal")


fig.canvas.draw()
pixels_per_AU = ax.transData.transform((1, 0))[0] - ax.transData.transform((0, 0))[0]
earth_diameter_pixels = 2 * (r / AU) * pixels_per_AU # PLANET SCALE: *10
earth_markersize = earth_diameter_pixels * 72 / fig.dpi 
ln.set_markersize(earth_markersize)

star_radius = sr / AU
star = {"center": (0, 0), "radius": star_radius} # r in [stellar radius] devided by stellar radius in AU


ax.add_patch(patches.Circle(star["center"], radius=star["radius"], color="#eca53c"))



def init():
     ax.set_xlim(-(scale), scale)  
     ax.set_ylim(-(scale), scale)     
     return ln,

def orbit(frame):

     t = frame /2 *speed
     M = 2 * math.pi * t / P
     E = calculate_E(M, e)

     x = a * math.sqrt(1 - e**2) * math.sin(E)
     y = 0

     ln.set_data([x], [y])

     return ln,

fps = 60
speed = 1
frames = math.floor(P*2/speed)

ani = FuncAnimation(fig, orbit, frames=frames, interval=1000/fps, init_func=init, blit=False)

# video = ani.to_html5_video()
# plt.close(fig)


# return video, round(planet_scale, ndigits=2), round(star_scale, ndigits=2), round(speed, ndigits=3)

plt.show()