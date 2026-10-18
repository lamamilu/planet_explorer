from flask import Flask, render_template, request
import requests

from utility import *
from planet_sim import *


app = Flask(__name__)
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

table = "pscomppars"
columns = ["pl_name", "pl_masse", "disc_telescope", "hostname", "discoverymethod", "disc_year", "pl_orbeccen", "pl_orbper", "pl_orbsmax", "st_rad", "pl_rade"]
constraints = ["pl_name = 'Kepler-10 b'"] # "pl_masse between 0.9 and 1.1", "discoverymethod = 'Transit'", "sy_snum = 1"


@app.route("/", methods=["GET", "POST"])
def home():

     query = url + adql(table, columns, constraints)
     response = requests.get(query)
     print(response.status_code)


     file = "templates/home.html"

     with open(file, "r", encoding="utf-8") as file:
          html_content = file.read()

     updated_html = html_content.replace("<!-- ANIMATION_PLACEHOLDER -->", orbit_animation(response.json()[0], 1))

     with open(file, "w", encoding="utf-8") as file:
          file.write(updated_html)

     plt.close()

     return render_template("home.html", planets=response.json())


app.run()