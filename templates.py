from flask import Flask,render_template,url_for,Markup
#import sqlalchemy
import json
import pandas as pd
import networkx as nx
import matplotlib.cm as cmm
import matplotlib.pyplot as plt
from Lib.SENTET import NLP 
from flask import request
from pandas import Timestamp
import numpy as np
from datetime import date, datetime

""" Library SENTET """
from Lib.TwitterConfig import *
from Lib.create_db import input_database as ID
from Lib.GrafGenerator import Grap_Generate as gg

import pymysql
pymysql.install_as_MySQLdb() 
import MySQLdb

pymysql.converters.encoders[Timestamp] = pymysql.converters.escape_datetime
pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.encoders[np.int64] = pymysql.converters._escape_table
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

con = MySQLdb.connect(user="root",passwd="",host="127.0.0.1",db="sentiment_analysis_twitter")
cursor = con.cursor(pymysql.cursors.DictCursor)
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["CACHE_TYPE"] = "Null" 
global cari

"""
LIST VARIABEL CSS
"""
list_css = [
    '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">',
]

"""
LIST VARIABEL JS
"""
list_js = [
    #'<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>',
    #'<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>',
    #'<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>'
    #'<script src="component/asset/head.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.min.js"></script>',
    '<script src="http://d3js.org/d3.v2.min.js?2.9.3"></script>'
    #'<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.bundle.min.js"></script>'
]

"""
Fungsi yang digunakan untuk merubah JSON
"""
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

"""
Call library Utama SENTET
"""
def SENTET(cari):
    twitter = login()
    global NLP
    NLP = NLP()
    dataaccum = NLP.MineData(twitter, cari ,2)
    #print(dataaccum)
    dp = NLP.ProsesStoreData(dataaccum)
    df = NLP.ProcessSentiment(dataaccum)
    dfs = NLP.ProcessHashtags(dataaccum)
    dft = NLP.ProcessTimestamp(dataaccum)
    #print("===================================================================== \n")
    
    """
    Proses Memasukan Data ke dalam Database sql
    """
    ID.masuk_tweet(dp[1]) #tabel tweet
    ID.masuk_retweet(dp[0]) #tabel retweet
    ID.sambungan(dp[1]) #tabel_cari
    #Export Grap dari Class Grap_Generate
    gg.Word(dp)
    return(dp)

def getDB(cari):
    sql = " SELECT tweet.Username, tweet.tanggal, tweet.tweet, tweet.SA FROM tweet \
            LEFT JOIN tabel_cari ON tabel_cari.idT = tweet.idT \
            LEFT JOIN hashtag ON hashtag.idH = tabel_cari.idH \
            WHERE hashtag.isi = %s;" #hashtag.isi = %s (nama hashtag)
    cursor.execute(sql,cari)
        
"""
Halaman Home Page
"""
@app.route("/", methods=['GET','POST'])
@app.route("/home")
def home():
    #dump(render_template("home.html"))
    #print(url_for('static', filename='ujicoba.css'))
    return render_template("component/body/home.html",list_css = list_css,list_js = list_js)

"""
Endpoint Search
"""
@app.route("/search",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        cari = request.form['search']
        dp = SENTET(cari)
        dpa = dp[2]   
        getDB(cari)
        hitung_tweet = len(dpa)
        #return redirect(url_for("component/body/hasil.html",list_css = list_css,list_js = list_js))
        return render_template("component/body/hasil.html",list_css = list_css,list_js = list_js, hitung_tweet = hitung_tweet, cari = cari)
    return cari

"""
Halaman About
"""
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/getApiAll")
def getApi():
    hs = cursor.fetchall()
    #print(hs)
    return json.dumps(hs, default=json_serial)
               

def prosesApiDate():
    pass

@app.route("/ujicoba")
def uji():
    return json.dumps(Markup.escape(render_template("ujicoba.html")))
    #return json.dumps(posts)

"""
Endpoint network node
"""
@app.route("/ujiTampilan/json")
def ujiTampilanJson():
    df = pd.read_csv('Lib/export/total.csv')
    #print(df)
    hasil = []
    for i in df.loc[:,'Hashtags']:
        if pd.isnull(i) is False:
            for j in str(i).split(" "):
                if j is not "":
                    hasil.append(j.lower())
    
    edge = []
    edge = list(set(hasil))
    link = []
    z = 0
    for i in df.loc[:,'Hashtags']:
        if pd.isnull(i) is False:
            for j in str(i).split(" "):
                if j is not "" and len(j) > 2:
                    for k in str(i).split(" "):
                        if k is not "" and len(k) > 2:
                            if j.lower() is not k.lower():
                                if len(link) > 0:
                                    for l in link:
                                        if l['source'] != edge.index(j.lower()) and l['target'] != edge.index(k.lower()):
                                            link.append({"source" : edge.index(j.lower()), "target": edge.index(k.lower()), "weight" : 1})
                                else:
                                    link.append({"source" : edge.index(j.lower()), "target": edge.index(k.lower()), "weight" : 1})

    #print(link)
    """
    link_new = []
    for i in link:
        if len(link_new) == 0:
            link_new.append(i)
        else:
            for j in link_new:
                if i['source'] != j['source'] and i['target'] != j['target']:
                    link_new.append(i)
    
    print(link_new)
    """
    hasil = []
    for i in edge:
        hasil.append({"name":i,"group":1})
    a = {
        "nodes":hasil,
        "links":link,
        "length":[len(hasil),len(link)]
    }
    return json.dumps(edge)

"""
Endpoint chart analys sentiment
"""
@app.route("/ujiChart/json")
def ujiChartJSON():
    df = pd.read_csv('Lib/export/total.csv')
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
    

if __name__ == '__main__':
    app.run(debug=True)