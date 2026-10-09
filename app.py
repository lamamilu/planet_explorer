from flask import Flask, render_template, request
import requests

from utility import *


app = Flask(__name__)
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

table = "pscomppars"
columns = ["pl_name", "pl_masse", "disc_telescope", "hostname", "discoverymethod", "disc_year"]
constraints = ["pl_masse between 0.9 and 1.1"]


@app.route("/", methods=["GET", "POST"])
def home():

     query = url + adql(table, columns, constraints)
     response = requests.get(query)
     print(response.status_code)

     return render_template("home.html", planets=response.json())


app.run()