from twython import Twython
import time
import collections
import pandas as pd
import numpy as np
import re
from os import path
from sqlalchemy import create_engine
from GrafGenerator import Grap_Generate
#from analiser import Analiser
from TwitterConfig import *

twitter = login()

#an = Analiser(training_data='data/coba_train.csv')

# load model
#filename='model'
#an.load_model(filename)

def MineData(apiobj, query, pagestocollect = 10):
    results = apiobj.search(q=query, include_entities='true',
                            tweet_mode='extended',count='450',
                            result_type='recent',
                            include_retweets=True)
    data = results['statuses']
    i=0
    ratelimit=1
    while results['statuses'] and i<pagestocollect: 
        if ratelimit < 1: 
            print(str(ratelimit)+'Rate limit!')
            break
        mid= results['statuses'][len(results['statuses']) -1]['id']-1
        print(mid)
        print('Jumlah Tweet : '+str(len(results['statuses'])))
        results = apiobj.search(q=query, max_id=str(mid)
                            ,include_entities='true',
                            tweet_mode='extended',count='450',
                            result_type='recent',
                            include_retweets=True)
        data+=results['statuses']
        i+=1
        ratelimit = int(apiobj.get_lastfunction_header('x-rate-limit-remaining'))
    return data

def tulis(data):
    for index, twit in enumerate(data):
        print(twit)
    #print(t)

def ProcessHashtags(data):
    HashtagData = pd.DataFrame(columns=['HT','ID','Date','RAWDATA_INDEX'])
    for index,twit in enumerate(data):
        HashtagData = HashtagData.append(pd.DataFrame({'ID':twit['id'],
                        'Date':pd.to_datetime(twit['created_at']),
                        'RAWDATA_INDEX':index,
                        'HT':[hashtag['text'] for hashtag 
                                in twit['entities']['hashtags']]})
                            , ignore_index=True)
    return HashtagData

def ProcessTimestamp(data):
    TimestampData = pd.DataFrame(columns=['ID','Date','RAWDATA_INDEX'])
    for index,twit in enumerate(data):
        TimestampData = TimestampData.append(pd.DataFrame({'ID':[twit['id']],
                        'Date':[pd.to_datetime(twit['created_at'])],
                        'RAWDATA_INDEX':[index]})
                            , ignore_index=True)
    return TimestampData

def hapus_katadouble(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return  pattern.sub(r"\1\1", s)

def clean_tweet(tweet):   
    #tweet=tweet.lower()
    tweet = re.sub(r'\\u\w\w\w\w', '', tweet)
    tweet = re.sub(r'http\S+','',tweet)# hapus link
    #tweet = re.sub(r'RT','',tweet)
    tweet = re.sub('@[^\s]+','',tweet)# hapus username
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)# hapus tagger
    tweet=re.sub(r'\w*\d\w*', '',tweet).strip() #hapus angka & str(angka) 
    tweet=hapus_katadouble(tweet) # lurus
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def ProcessSentiment(data):
    SentimentData = pd.DataFrame(columns=['ID','Date','Polarity'], dtype = float)    
    for index,twit in enumerate(data):
        SentimentData = SentimentData.append(pd.DataFrame({'ID':[twit['id']],
                        'Date':[pd.to_datetime(twit['created_at'])],
                        'Polarity':[an.testFromTrained([an.tfidf_data.transform(twit['full_text'])])]})
                            , ignore_index=True)
    return SentimentData

def ProsesStoreData(data):
    df1 = pd.DataFrame(columns=['IDrts', 'IDR', 'Username', 'Date', 'Retweet', 'Hashtags', 'RT', 'SA', 'Float'])
    df2 = pd.DataFrame(columns=['ID', 'Username', 'Date', 'Tweet', 'Hashtags', 'RT', 'SA', 'Float'])
    for index, twit in enumerate(data):
        a = ''
        b = ''
        c = ''
        for hashtag in twit['entities']['hashtags']:
            if hashtag['text'] is None:
                a = ' '
            else:
                a = a + str(hashtag['text'] + ' ')
        if 'retweeted_status' in twit:
        
            df1 = df1.append(pd.DataFrame({
                'IDrts':[pd.to_numeric(twit['retweeted_status']['id'], downcast='signed')],
                'IDR':[pd.to_numeric(twit['id'])],
                'Username':[twit['user']['screen_name']],
                'Date':[pd.to_datetime(twit['created_at'])],
                'Retweet':[clean_tweet(twit['full_text'])],
                'Hashtags':[a],
                'RT':[twit['retweet_count']],
                'SA':[an.testStrFromTrained([an.tfidf_data.transform(twit['full_text'])])],
                'Float':[float(an.testFromTrained([an.tfidf_data.transform(twit['full_text'])]))]
            }))
            #b = clean_tweet(twit['full_text'])
        else:
            df2 = df2.append(pd.DataFrame({
                'ID':[pd.to_numeric(twit['id'], downcast='signed')],
                'Username':[twit['user']['screen_name']],
                'Date':[pd.to_datetime(twit['created_at'])],
                'Tweet':[clean_tweet(twit['full_text'])],
                'Hashtags':[a],
                'RT':[twit['retweet_count']],
                'SA':[an.testStrFromTrained([an.tfidf_data.transform(twit['full_text'])])],
                'Float':[float(an.testFromTrained([an.tfidf_data.transform(twit['full_text'])]))]
            }))
    df1.to_csv('export/RT.csv')
    df2.to_csv('export/T.csv')
    #print(df1)
    StoreData = [df1, df2]
    #print(StoreData[0])
    print("Proses Crawl Data Selesai! \n")
    return StoreData

def debugging(text,i):
    print("---------------------------pyt------------[",str(i),"]-------------------------------")
    print(text)
    print("----------------------------------------------------------------------------------")

if __name__ == '__main__':
    #cari = input('Masukan Kata Kunci > ')
    #dataaccum = MineData(twitter, cari, 2)

    #test
    #global dp
    #global df
    #global dfs
    #global dft


    #tulis(dataaccum)

    #dps = seleksi_data_rt(dp)
    #df = ProcessSentiment(dataaccum)
    #dfs = ProcessHashtags(dataaccum)
    #dft = ProcessTimestamp(dataaccum)

    df = pd.read_csv('export/out.csv')
    #print(df)
    
    #debugging(df.loc[:,'Hashtags'],1)
    hasil = []
    for i in df.loc[:,'Hashtags']:
        if pd.isnull(i) is False:
            for j in str(i).split(" "):
                if j is not "":
                    hasil.append(j.lower())
    
    import networkx as nx
    import matplotlib.cm as cmm
    import matplotlib.pyplot as plt
    G = nx.Graph()
    G.clear()   
    
    for i in hasil:
        G.add_node(i,name=i)
    
    edges = []

    for i in df.loc[:,'Hashtags']:
        if pd.isnull(i) is False:
            for j in str(i).split(" "):
                if j is not "" and len(j) > 2:
                    for k in str(i).split(" "):
                        if k is not "" and len(k) > 2:
                            if j.lower() is not k.lower():
                                edges.append([j.lower(),k.lower()])
    
    debugging(edges,3)
    for edge in edges:
        G.add_edge(edge[0],edge[1])

    nx.draw(G, node_size=1600, cmap=cmm.get_cmap('Reds'), node_color=range(len(G)), pos=nx.random_layout(G), with_labels=True)
    plt.show()

    #from create_db import *
    #from create_db2 import *
    #uh = has_dup(dp)
    #masuk_hashtag(dp)
    #masuk_tweet(dp[1])
    #masuk_retweet(dp[0])
    #sambungan(dp[1])
    #ke_sql(dp)

    #table_tweet(dp)


    #gg = Grap_Generate
    #gg.PieChart(dp)
    #gg.Graf(df, dfs, dft)
    #gg.Word(dp)
    #gg.Node(dp)