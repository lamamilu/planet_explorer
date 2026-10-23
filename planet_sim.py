import matplotlib
matplotlib.use("Agg")

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

def orbit_animation(p, speed):

     # *********** DATA ***********

     def calculate_E(M, e):
          E = M
          for i in range(10):
               E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
          return E

     r = p["pl_rade"]
     sr = p["st_rad"]

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



     width = 7
     height = 7

     scale = a * 1.1
     x_min = scale + a*e
     x_max = scale - a*e

     fig, ax = plt.subplots(figsize=(width, height))
     plt.plot(ellipse_x, ellipse_y, label='Orbit outline', color='green')
     ln, = ax.plot([], [], 'o', color='blue')
     ax.set_xlim(-(x_min), x_max) 
     ax.set_ylim(-(scale), scale)
     ax.set_aspect("equal")


     fig.canvas.draw()
     pixels_per_AU = ax.transData.transform((1, 0))[0] - ax.transData.transform((0, 0))[0]
     earth_diameter_pixels = 2 * (r * 6371 / AU * 10) * pixels_per_AU # PLANET SCALE: *10
     earth_markersize = earth_diameter_pixels * 72 / fig.dpi 
     if earth_markersize < 8:
          earth_markersize = 8
     ln.set_markersize(earth_markersize)

     sun_radius = sr * 695700 / AU
     if sun_radius < scale / 20:
          sun_radius = scale / 20
     star = {"center": (0, 0), "radius": sun_radius} # r in [stellar radius] devided by stellar radius in AU
     ax.add_patch(patches.Circle(star["center"], radius=star["radius"], color="#eca53c"))



     def init():
          ax.set_xlim(-(x_min), x_max)  
          ax.set_ylim(-(scale), scale)     
          return ln,

     def orbit(frame):
     
          t = frame /2 *speed
          M = 2 * math.pi * t / P
          E = calculate_E(M, e)

          x = a * (math.cos(E) - e)
          y = a * math.sqrt(1 - e**2) * math.sin(E)

          ln.set_data([x], [y])

          return ln,

     fps = 60

     ani = FuncAnimation(fig, orbit, frames=math.floor(P*2/speed), interval=1000/fps, init_func=init, blit=False)

     video = ani.to_html5_video()
     plt.close(fig)
     return video

     # plt.show()