from flask import Flask,render_template,url_for,Markup
#import sqlalchemy
import json
import pandas as pd
import networkx as nx
import matplotlib.cm as cmm
import matplotlib.pyplot as plt
#from Lib.SENTET import NLP
from flask import request

app = Flask(__name__)

#
# LIST VARIABEL CSS
#
list_css = [
    '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">',
]

#
# LIST VARIABEL JS
#
list_js = [
    #'<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>',
    #'<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>',
    #'<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>'
    #'<script src="component/asset/head.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>',
    '<script src="http://d3js.org/d3.v2.min.js?2.9.3"></script>'
    #'<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.bundle.min.js"></script>'
]

posts = [
    {
        'author'      : 'Corey Schafer',
        'title'       : 'Blog Post 1',
        'content'     : 'First post content',
        'date_posted' : 'April 20, 2019',
        #'css'         : url_for('static', filename='ujicoba.css')
    },
    {
        'author'      : 'Jane Doe',
        'title'       : 'Blog Post 2',
        'content'     : 'Second post content',
        'date_posted' : 'April 21, 2019',
        #'css'         : url_for('static', filename='ujicoba.css')
    }
]

@app.route("/", methods=['GET','POST'])
@app.route("/home")
def home():
    #dump(render_template("home.html"))
    #print(url_for('static', filename='ujicoba.css'))
    return render_template("component/body/home.html",list_css = list_css,list_js = list_js)


@app.route("/search",methods=['GET','POST'])
def index():
    print(request)
    #return json.dumps(request)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/user/<username>")
def show_post(username):
    return "User %s" % username


@app.route("/subpath/<path:user_path>")
def show_subpath(user_path):
    return "Path %s" % user_path


@app.route("/ujicoba")
def uji():
    return json.dumps(Markup.escape(render_template("ujicoba.html")))
    #return json.dumps(posts)


@app.route("/ujiTampilan")
def ujiTampilan():
    return render_template("component/body/coba.html")

@app.route("/ujiTampilan/json")
def ujiTampilanJson():
    df = pd.read_csv('Lib/export/out.csv')
    #print(df)
    hasil = []
    for i in df.loc[:,'Hashtags']:
        if pd.isnull(i) is False:
            for j in str(i).split(" "):
                if j is not "":
                    hasil.append(j.lower())
    
    edge = []

    edge = list(set(hasil))

    #for i in range(0,len(hasil)):
    #    if len(edge) > 0:
    #        length = len(edge)
    #        print(length)
    #        for j in range(0,length):
    #            if hasil[i] is not edge[j]:
    #                edge.append(hasil[i])
    #    else:
    #        edge.append(hasil[i])
    #        print(edge)
    
    #print(edge)
    link = []
    for i in df.loc[:,'Hashtags']:
        if pd.isnull(i) is False:
            for j in str(i).split(" "):
                if j is not "" and len(j) > 2:
                    for k in str(i).split(" "):
                        if k is not "" and len(k) > 2:
                            if j.lower() is not k.lower():
                                link.append({"source" : edge.index(j.lower()), "target": edge.index(k.lower()), "weight" : 1})
    
    hasil = []
    for i in edge:
        hasil.append({"name":i,"group":1})
    a = {
        "nodes":hasil,
        "links":link,
        "length":[len(hasil),len(link)]
    }
    """a = {
        "nodes":[
            {"name":"node1","group":1},
            {"name":"node2","group":2},
            {"name":"node3","group":2},
            {"name":"node4","group":3}
        ],
        "links":[
            {"source":2,"target":1,"weight":3},
            {"source":0,"target":2,"weight":3},
            {"source":0,"target":2,"weight":3}
        ]
    }"""
    return json.dumps(a)

@app.route("/ujiChart/json")
def ujiChartJSON():
    df = pd.read_csv('Lib/export/out.csv')
    #print(df)
    hasil = []
    a = 0
    b = 0
    c = 0 
    #print(df.loc[:,'SA'])
    for i in df.loc[:,'SA']:
        #print(i)
        if i == "Positif":
            a = a + 1
        elif i == "Negatif":
            b = b + 1
        elif i == "Netral":
            c += 1
    hasil = {
        "P" : a,
        "N" : b,
        "L" : c
    }
    print(hasil)
    return json.dumps(hasil)
    

with app.test_request_context():
    print(url_for('show_post',username="John Cena"))
    print(url_for('about'))

if __name__ == '__main__':
    app.run(debug=True)