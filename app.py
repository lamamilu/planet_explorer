from flask import Flask, render_template, request
import requests

from utility import *


app = Flask(__name__)
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="

table = "ps"
columns = ["pl_name", "pl_masse"]
constraints = ["pl_masse between 0.9 and 1.1"]


@app.route("/", methods=["GET", "POST"])
def home():

     query = url + adql(table, columns, constraints)
     response = requests.get(query)

     return render_template("home.html", adql=response.json())


app.run()