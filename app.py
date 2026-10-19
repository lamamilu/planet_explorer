from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os
import json

from utility import *
from planet_sim import *



if os.path.exists("planets.json") and os.path.getsize("planets.json")!=0:
     with open("planets.json", "r") as f:
          planets = json.load(f)
else:
     planets = {}


app = Flask(__name__)
app.secret_key = "planets!"

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

table = "pscomppars"
columns = ["pl_name", "pl_masse", "disc_telescope", "hostname", "discoverymethod", "disc_year", "pl_orbeccen", "pl_orbper", "pl_orbsmax", "st_rad", "pl_rade"]
# constraints = ["pl_name = 'Kepler-10 b'"] # "pl_masse between 0.9 and 1.1", "discoverymethod = 'Transit'", "sy_snum = 1"


@app.route("/", methods=["GET", "POST"])
def home():

     print("\n-----------------------------------------------------------------\n")

     planet = "16 Cyg B b"

     print("looking for planet:", planet)


     if planet in planets:
          print("planet FOUND in planets.json\nLOADING PLANET FROM PLANETS.JSON")
          data = planets[planet]
     else:
          print("planet NOT FOUND in planets.json\nREQUESTING PLANET FROM NASA")
          constraints = [f"pl_name = '{planet}'"]
          query = url + adql(table, columns, constraints)
          response = requests.get(query)
          print(response.status_code)
          planets[planet] = response.json()[0]
          update_planets(planets)

          data = response.json()[0]

          if response.status_code != 200:
               session["message"] = response.text[:2000]
               return redirect(url_for("error", code = response.status_code))


     speed=1
     if request.method == "POST":
          action = request.form.get("action")
          if action == "set-speed":
               speed = int(request.form.get("speed"))
               speed = convert_speed(speed)

     print("speed:", speed)
     ani = orbit_animation(data, speed)

     ani_list = ani.split('width="700" height="700"')
     animation = ani_list[0] + 'width="400" height="400"' + ani_list[1]

     return render_template("home.html", planet=data, animation=animation)


@app.route("/error/<code>", methods=["GET", "POST"])
def error(code):
     return render_template("error.html", code=code, message=session.pop("message", None))



app.run()

