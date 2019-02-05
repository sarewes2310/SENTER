from flask import Flask
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json
app = Flask(__name__)

@app.route("/hello")
def hello():
    try:
        #print(render_template("./coba_1.html"))
        return render_template("hello/coba_1.html")
    except TemplateNotFound:
        abort(404)

# Halaman index
@app.route("/")
def index():
    return "Mantap Jiwa" + coba()

def coba():
    return "KASKUS"

@app.route("/Data")
def Data():
    return json.dumps({'a' : 1,'b' : 2,'c' : 3})