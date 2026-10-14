import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import math

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro')

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


sun = {"center": (0, 0), "radius": .2, "color": "#eca53c"}
earth = {"center": (0, 0), "radius": .2, "color": "blue"}

#for data in circle_data:
     #circle = patches.Circle(data["center"], radius=data["radius"], color=data["color"], alpha=0.5)
     #ax.add_patch(circle)



def init():
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    return ln,

def orbit(frame):
    ax.add_patch(patches.Circle(sun["center"], radius=sun["radius"], color=sun["color"], alpha=0.5))
    
    t = frame * 3
    M = 2 * math.pi * t / P
    E = calculate_E(M, e)

    x = a * (math.cos(E) - e)
    y = b * math.sin(E)

    ln.set_data([x], [y])

    return ln,

ani = FuncAnimation(fig, orbit, frames=1000, init_func=init, blit=False)
plt.show()