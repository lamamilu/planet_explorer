from flask import Flask, render_template, request, redirect, url_for, session
import requests

from utility import *
from planet_sim import *


app = Flask(__name__)
app.secret_key = "planets!"

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

table = "pscomppars"
columns = ["pl_name", "pl_masse", "disc_telescope", "hostname", "discoverymethod", "disc_year", "pl_orbeccen", "pl_orbper", "pl_orbsmax", "st_rad", "pl_rade"]
constraints = ["pl_name = 'Kepler-10 b'"] # "pl_masse between 0.9 and 1.1", "discoverymethod = 'Transit'", "sy_snum = 1"


@app.route("/", methods=["GET", "POST"])
def home():

     query = url + adql(table, columns, constraints)
     response = requests.get(query)
     print(response.status_code)

     if response.status_code != 200:
          session["message"] = response.text[:2000]
          return redirect(url_for("error", code = response.status_code))


     ani = orbit_animation(response.json()[0], 1)

     ani_list = ani.split('width="700" height="700"')
     animation = ani_list[0] + 'width="400" height="400"' + ani_list[1]

     return render_template("home.html", planets=response.json(), animation=animation)


@app.route("/error/<code>", methods=["GET", "POST"])
def error(code):
     return render_template("error.html", code=code, message=session.pop("message", None))



app.run()

