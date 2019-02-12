from twython import Twython
import time
import collections
import pandas as pd
import numpy as np
import re
from os import path
from sqlalchemy import create_engine
from analiser import Analiser
from TwitterConfig import *

"""
Main Program yang berfungsi mencrawl data twitter 
dan menjadikan 2 data besar Tweet dan Retweet 

Note: model dapat ditraining, atau di-load, atau di retrain 

an = Analiser(training_data='data/coba_train.csv')

#Training :
filename='model'
an.train(filename)

#Load:
filename = 'model'
an.load_model(filename)

#Retrain:
filename = 'model'
an.retrain(filename)

#Contoh Print Hasil Sentimen :
kata1 = input() 
print (an.testFromTrained([an.tfidf_data.transform(kata1)])) #float
print (an.testFromTrained([an.tfidf_data.transform(kata2)])) #Pos, Net, Neg
"""

twitter = login() #load TwitterConfig 

#Memanggil Class Analiser untuk load data set


class NLP:

    def __init__(self, param, model):
        an = Analiser(training_data='data/coba_train.csv')
        # load model
        self.model = model
        
        if model == 'load_model':
            filename='model'
            an.load_model(filename)
        
        elif model == 'train_model':
            filename='model'
            an.train(filename)

        elif model == 'retrain':
            filename='model'
            an.retrain(filename)
        else:
            exit()

        self.instance_var1 = param
    
    def create_var(self):
      pass  

    """
    Mencrawl twitter Data
    """

    def MineData(self, apiobj, query, pagestocollect = 10):

        results = apiobj.search(q=self.instance_var1, include_entities='true',
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
            
            mid = results['statuses'][len(results['statuses']) -1]['id']-1

            print(mid)
            print('Jumlah Tweet Per-page : '+str(len(results['statuses'])))
            
            results = apiobj.search(q=self.instance_var1, max_id=str(mid)
                                ,include_entities='true',
                                tweet_mode='extended',count='450',
                                result_type='recent',
                                include_retweets=True)
            
            data+=results['statuses']
            i+=1
            ratelimit = int(apiobj.get_lastfunction_header('x-rate-limit-remaining'))

        print(data)
        return data

    """
    ProcessHashtags berfungsi mengambil hanya 
    hashtag
    """

    def ProcessHashtags(self, data):
        HashtagData = pd.DataFrame(columns=['HT','ID','Date','RAWDATA_INDEX'])
        
        for index,twit in enumerate(data):
            HashtagData = HashtagData.append(pd.DataFrame({'ID':twit['id'],
                            'Date':pd.to_datetime(twit['created_at']),
                            'RAWDATA_INDEX':index,
                            'HT':[hashtag['text'] for hashtag 
                                    in twit['entities']['hashtags']]})
                                , ignore_index=True)

        return HashtagData
    """
    ProcessTimestamp berfungsi mengambil data timestamp 
    untuk data pada Class Grap_Generate
    """
    def ProcessTimestamp(self, data):
        TimestampData = pd.DataFrame(columns=['ID','Date','RAWDATA_INDEX'])
        
        for index,twit in enumerate(data):
            TimestampData = TimestampData.append(pd.DataFrame({'ID':[twit['id']],
                            'Date':[pd.to_datetime(twit['created_at'])],
                            'RAWDATA_INDEX':[index]})
                                , ignore_index=True)

        return TimestampData

    """
    clean_tweet berfungsi normalisasi tweet sebelum masuk ke DataFrame
    """

    def clean_tweet(tweet):   
        
        def hapus_katadouble(s):
            pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
            return  pattern.sub(r"\1\1", s)
        
        #tweet=tweet.lower()
        tweet = re.sub(r'\\u\w\w\w\w', '', tweet)
        tweet = re.sub(r'http\S+','',tweet)# hapus link
        #tweet = re.sub(r'RT','',tweet)
        tweet = re.sub('@[^\s]+','',tweet)# hapus username
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)# hapus tagger
        tweet=re.sub(r'\w*\d\w*', '',tweet).strip() #hapus angka & str(angka) 
        tweet=hapus_katadouble(tweet) # lurus
        
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    """
    ProcessSentiment mengolah data sentimen berdasarkan crawl tweet,
    kemudian data sentiment tersebut digunakan pada 
    Class Graph_Generate  
    """

    def ProcessSentiment(self, data):
        SentimentData = pd.DataFrame(columns=['ID','Date','Polarity'], dtype = float)
        
        for index,twit in enumerate(data):
            SentimentData = SentimentData.append(pd.DataFrame({'ID':[twit['id']],
                            'Date':[pd.to_datetime(twit['created_at'])],
                            'Polarity':[an.testFromTrained([an.tfidf_data.transform(twit['full_text'])])]})
                                , ignore_index=True)

        return SentimentData
    """
    ProsesStoreData berfungsi sebagai mengubah data crawl menjadi DataFrame,
    dan membagi 2 besar data menjadi Data tweet, dan data Retweet
    """

    def ProsesStoreData(self, data):
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
                    'IDrts':[(twit['retweeted_status'])],
                    'IDR':[(twit['id'])],
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
                    'ID':[(twit['id_str'])],
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
        return self.StoreData

    #input query yang akan di search
  
    #cari = self.query

obj1 = NLP('2019GantiPresiden', 'train_model') 

dataaccum = obj1.MineData(twitter, obj1.instance_var1, 2)

#test
#global dp
#global df
#global dfs
#global dft

dp = ProsesStoreData(dataaccum)
df = ProcessSentiment(dataaccum)
dfs = ProcessHashtags(dataaccum)
dft = ProcessTimestamp(dataaccum)

"""
Proses Memasukan Data ke dalam Database sql
"""
from create_db import input_database as ID

ID.masuk_tweet(dp[1]) #tabel tweet
ID.masuk_retweet(dp[0]) #tabel retweet
ID.sambungan(dp[1]) #tabel_cari

"""
Export Grap dari Class Grap_Generate
"""
from GrafGenerator import Grap_Generate

#gg = Grap_Generate
#gg.PieChart(dp)
#gg.Graf(df, dfs, dft)
#gg.Word(dp)
#gg.Node(dp)

#print(obj.instance_var1)