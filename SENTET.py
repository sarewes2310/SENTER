import json
import pandas as pd
import networkx as nx
import matplotlib.cm as cmm
import matplotlib.pyplot as plt
from pandas import Timestamp
import numpy as np
from datetime import date, datetime
from twython import Twython
from Lib.create_db import input_database 
#import Lib.create_db
from Lib.GrafGenerator import Grap_Generate as gg

class SENTET:
    def login_twitter(CONSUMER_KEY='qXVo3PXRvaxRDinwEqluagyGB', CONSUMER_SECRET='8vkWXs30seGMJeJ21tg5SXXY0Lry9kdYhvJEGS3mYXIE6LHHpp', 
        ACCESS_TOKEN='1707115609-D1axGwQkv2Mn2NOXd1sHqZbnQx0DqIJoHANI26V', ACCESS_SECRET='liUdv7bkjUAWB347pl4oPfjhwlsHdzlAOn9fee6MoFhGL'):
        key = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
        return key

    def pencarian(cari, key):
        from Lib.NLP import NLP 
        twitter = key
        NLP = NLP()
        getminedata = NLP.MineData(twitter, cari ,2)
        dp = NLP.ProsesStoreData(getminedata)
        df = NLP.ProcessSentiment(getminedata)
        dfs = NLP.ProcessHashtags(getminedata)
        dft = NLP.ProcessTimestamp(getminedata)
        
        """
        Proses Memasukan Data ke dalam Database sql
        """
        ID = input_database()
        ID.masuk_tweet(dp[1]) #tabel tweet
        ID.masuk_retweet(dp[0]) #tabel retweet
        #ID.sambungan(dp[1]) #tabel_cari

        #Export Grap dari Class Grap_Generate
        #gg.Word(dp)
        return(dp) 

    def graph_network(cari):
        hasil = []
        hasil_all = []
        """
        Bentuk data
        hasil = ['pondokpinang','pasfriend','dll']
        """
        ID = input_database()
        tweet = ID.select_tweet()
        hasil_all['node'] = ID.select_hashtag()
        for i in hasil_all['node']:
            select_network = ID.select_network();
            if len(select_network) > 2:
                for j in select_network:
                    print('database')
            if len(search_network) == 2:
                print("database")
        hasil_all['edge'] = hasil
        return hasil_all
        """
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

        hasil = []
        for i in edge:
            hasil.append({"name":i,"group":1})
        a = {
            "nodes":hasil,
            "links":link,
            "length":[len(hasil),len(link)]
        }
        """
    ### TESTING ###
    def word_cloud_generate():
        ID = input_database()
        tweet = ID.select_tweet()
        retweet = ID.select_retweet()
        hasil = []
        for i in tweet:
            hasil.append(i['tweet'])
        for j in retweet:
            hasil.append(j['retweet'])
        image = gg.Word(hasil)
        data = {
            'link' : image
        }
        return data

    ### TESTING ###
    def word_cloud_generate_by_date(cari):
        ID = input_database()
        tweet = ID.select_tweet_date(cari[0],cari[1])
        retweet = ID.select_retweet_date(cari[0],cari[1])
        hasil = []
        for i in tweet:
            hasil.append(i['tweet'])
        for j in retweet:
            hasil.append(j['retweet'])
        image = gg.Word(hasil)
        data = {
            'link' : image
        }
        return data

    ### TESTING ###
    def chart_analysis_generate():
        ID = input_database()
        hasil = []
        tweet = ID.select_tweet()
        retweet = ID.select_retweet()
        for i in tweet:
            hasil.append(i['SA'])
        for j in retweet:
            hasil.append(j['SA'])
        return hasil

    ### TESTING ###
    def chart_analysis_generate_by_date(cari):
        ID = input_database()
        hasil = []
        tweet = ID.select_tweet_date(cari[0],cari[1])
        retweet = ID.select_retweet_date(cari[0],cari[1])
        for i in tweet:
            hasil.append(i['SA'])
        for j in retweet:
            hasil.append(j['SA'])
        return hasil