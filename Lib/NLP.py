import time
import collections
import pandas as pd
import numpy as np
import re
from os import path
from sqlalchemy import create_engine

""" Library SENTET """
from .analiser import Analiser
#from .TwitterConfig import *
from .cleantweet import CleanTweet #cuma import fungsi clean_tweet()

class NLP:
    an = None
    def __init__(self):
        NLP.an = Analiser(training_data='Lib/data/coba_train.csv')
        filename = 'model'
        NLP.an.load_model(filename)
    
    """
    Crawl twitter Data
    """
    def MineData(self, apiobj, query, pagestocollect = 10):
        results = apiobj.search(q=query, include_entities='true',
                                tweet_mode='extended',count='450',
                                result_type='recent',
                                include_retweets=True)
        data = results['statuses']
        i=-1
        ratelimit=1
        while results['statuses'] and i < pagestocollect: 
            if ratelimit < 1: 
                print(str(ratelimit)+'Rate limit!')
                break
            mid = results['statuses'][len(results['statuses']) -1]['id']-1
            print(mid)
            print('Jumlah Tweet Per-page : '+str(len(results['statuses'])))
            results = apiobj.search(q=query, max_id=str(mid)
                                ,include_entities='true',
                                tweet_mode='extended',count='450',
                                result_type='recent',
                                include_retweets=True)
            data+=results['statuses']
            i+=1
            ratelimit = int(apiobj.get_lastfunction_header('x-rate-limit-remaining'))
        #print(data)
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
    ProcessSentiment mengolah data sentimen berdasarkan crawl tweet,
    kemudian data sentiment tersebut digunakan pada 
    Class Graph_Generate  
    """
    def ProcessSentiment(self, data):
        SentimentData = pd.DataFrame(columns=['ID','Date','Polarity'], dtype = float)
        for index,twit in enumerate(data):
            SentimentData = SentimentData.append(pd.DataFrame({'ID':[twit['id']],
                            'Date':[pd.to_datetime(twit['created_at'])],
                            'Polarity':[NLP.an.testFromTrained([NLP.an.tfidf_data.transform(twit['full_text'])])]})
                                , ignore_index=True)
        return SentimentData
    
    """
    ProsesStoreData berfungsi sebagai mengubah data crawl menjadi DataFrame,
    dan membagi 2 besar data menjadi Data tweet, dan data Retweet
    """
    def ProsesStoreData(self, data):
        #Note (Penting:)
        #jika terjadi : "TypeError: clean_tweet() missing 1 required positional argument: 'tweet'"
        #atau NameError: name 'an' is not defined
        #kemungkinan class belum diload, atau sudah diload
        CT = CleanTweet()
        df1 = pd.DataFrame(columns=['retweeted_status', 'ID', 'Username', 'Date', 'Tweet', 'Hashtags', 'RT', 'SA', 'Float'])
        df2 = pd.DataFrame(columns=['IDJsonT', 'Username', 'Date', 'Tweet', 'Hashtags', 'RT', 'SA', 'Float'])
        for index, twit in enumerate(data):
            a = ''
            b = ''
            c = ''
            value_training = [NLP.an.tfidf_data.transform(twit['full_text'])]
            for hashtag in twit['entities']['hashtags']:
                if hashtag['text'] is None:
                    a = ' '
                else:
                    a = a + str(hashtag['text'] + ' ')
                    a = a.lower()
            if 'retweeted_status' in twit:
                df1 = df1.append(pd.DataFrame({
                    'retweeted_status':[(twit['retweeted_status'])],
                    'ID':[(twit['id'])],
                    'Username':[twit['user']['screen_name']],
                    'Date':[pd.to_datetime(twit['created_at'])],
                    'Tweet':[CT.clean_text_tweet(twit['full_text'])],
                    'Hashtags':[a],
                    'RT':[twit['retweet_count']],
                    'SA':[NLP.an.testStrFromTrained(value_training)],
                    'Float':[float(NLP.an.testFromTrained(value_training))]
                }))                
                #b = clean_tweet(twit['full_text'])
            else:  
                #print(twit['full_text'])          
                df2 = df2.append(pd.DataFrame({
                    'IDJsonT':[(twit['id'])],
                    'Username':[twit['user']['screen_name']],
                    'Date':[pd.to_datetime(twit['created_at'])],
                    'Tweet':[CT.clean_text_tweet(twit['full_text'])],
                    'Hashtags':[a],
                    'RT':[twit['retweet_count']],
                    'SA':[NLP.an.testStrFromTrained(value_training)],
                    'Float':[float(NLP.an.testFromTrained(value_training))]
                }))

        #DataJoin = df1[['ID','Username', 'Date', 'Tweet', 'Hashtags', 'RT', 'SA', 'Float']].concat(df2[['ID','Username', 'Date', 'Tweet', 'Hashtags', 'RT', 'SA', 'Float'], on = 'ID')
        #DataJoin = pd.merge(df1, df2, how='inner', left_on = 'ID', right_on = 'ID') 
        DataJoin = pd.concat([df1, df2], sort=False)
        StoreData = [df1, df2, DataJoin]
        df1.to_csv('Lib/export/RT.csv')
        df2.to_csv('Lib/export/T.csv')
        DataJoin.to_csv('Lib/export/total.csv')
        return StoreData