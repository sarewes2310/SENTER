from sqlalchemy import create_engine 
import sys
import pandas as pd
import os 
import pandas.io.sql 
import numpy as np
from pandas import Timestamp
from datetime import datetime 
from collections import OrderedDict
from nltk.tokenize import word_tokenize
import re

import pymysql
pymysql.install_as_MySQLdb() 
import MySQLdb

pymysql.converters.encoders[Timestamp] = pymysql.converters.escape_datetime
pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.encoders[np.int64] = pymysql.converters._escape_table
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

con = MySQLdb.connect(user="root",passwd="",host="localhost",db="coba")
cursor = con.cursor(pymysql.cursors.DictCursor)

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
Fungsi untuk menginputkan data kedalam Database
"""

def input_tweet(sd, a):
    sqli = """
    INSERT INTO `tweet` 
    (`idJsonT`, `tweet`, `tanggal`, `Username`, `RT`, `SA`) 
    VALUES (%s, %s, %s, %s, %s, %s);"""
                            
    cursor.execute(sqli,(

    sd.iloc[a,0], #ID tweet
    sd.iloc[a,3], #tweet
    sd.iloc[a,2], #Date
    sd.iloc[a,1], #User
    sd.iloc[a,5], #Retweet Count
    sd.iloc[a,6]))#SA "pos, net, neg"

    con.commit()
    
    

def input_retweet(sdr, a, hasrtj):
        sqli = """
        INSERT INTO `retweet` 
        (`idT`, `idJsonR`, `tanggal`, `Username`, `retweet`, `RT`, `SA`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s);"""

        #print(i['idT'])
        #a = i['idT']
        cursor.execute(sqli,(

        hasrtj[0]['idT'],  #idT
        sdr.iloc[a,1],  #IDRetweet 
        sdr.iloc[a,3], #Tanggal
        sdr.iloc[a,2], #Username
        sdr.iloc[a,4], #Retweet
        sdr.iloc[a,6], #RT
        sdr.iloc[a,7]))#SA "pos, net, neg

        con.commit()

def input_rt_t(sdr, a):
        sqli = """
        INSERT INTO `tweet` 
        (`idJsonT`, `tweet`, `tanggal`, `Username`, `RT`, `SA`)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        #print(sdr.iloc[a,0]['id'])
        cursor.execute(sqli,(
        str(sdr.iloc[a,0]['id']), #ID tweet
        clean_tweet((sdr.iloc[a,0])['full_text']), #tweet
        sdr.iloc[a,0]['created_at'], #Date
        sdr.iloc[a,0]['user']['screen_name'], #User
        sdr.iloc[a,0]['retweet_count'], #Retweet Count
        sdr.iloc[a,7]))#SA "pos, net, neg"

        con.commit()
        
def input_sambungan(hs, hast): #(IDtweet, IDhashtag)

        sqli = """
        INSERT INTO `tabel_cari` 
        (`idT`, `idH`)
        VALUES (%s, %s)
        """
        cursor.execute(sqli, (
        hs[0]['idT'], # ID twitter 
        hast[0]['idH'])) #ID Hashtag
        
        con.commit()