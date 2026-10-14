import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import math

# *********** DATA ***********

def calculate_E(M, e):
    E = M
    for _ in range(10):
        E = E - (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    return E

a = 1.0             # AU
e = 0.0167
P = 365.256         # days
b = a * math.sqrt(1 - e**2)

t = 0               # days since perihelion
M = 2 * math.pi * t / P
E = calculate_E(M, e)

x = a * (math.cos(E) - e)
y = b * math.sin(E)

def calculate_x():
    return a * (math.cos(E) - e)
def calculate_y():
    return a * math.sqrt(1 - math.pow(e, 2)) * math.sin(E)


#for data in circle_data:
     #circle = patches.Circle(data["center"], radius=data["radius"], color=data["color"], alpha=0.5)
     #ax.add_patch(circle)

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'o', color='blue')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)

AU = 149597871
pixels_per_AU = ax.transData.transform((1, 0))[0] - ax.transData.transform((0, 0))[0]
earth_diameter_pixels = 2 * (6371 / AU * 100) * pixels_per_AU
earth_markersize = earth_diameter_pixels * 72 / fig.dpi
ln.set_markersize(earth_markersize)

sun = {"center": (0, 0), "radius": 696340 / AU, "color": "#eca53c"}




def init():
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    return ln,

def orbit(frame):
    ax.add_patch(patches.Circle(sun["center"], radius=sun["radius"], color=sun["color"]))
    
    t = frame * 3
    M = 2 * math.pi * t / P
    E = calculate_E(M, e)

    x = a * (math.cos(E) - e)
    y = b * math.sin(E)

    ln.set_data([x], [y])

    return ln,

ani = FuncAnimation(fig, orbit, frames=1000, init_func=init, blit=False)
plt.show()