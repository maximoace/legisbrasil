from flask import Flask
from flask import render_template, jsonify

from legisbrasil.database.database import Database

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/fetchTable")
def fetchTable():
    data = Database().read_basic()
    return data

@app.route("/details/<id>")
def details(id):
    data = Database().read_detailed(id)
    return render_template('details.html', data=data)