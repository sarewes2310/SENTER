from sqlalchemy import create_engine 
import sys
import pandas as pd
import os 
import pandas.io.sql 
import numpy as np
from collections import OrderedDict
from nltk.tokenize import word_tokenize

import pymysql
pymysql.install_as_MySQLdb() 
import MySQLdb

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

con = MySQLdb.connect(user="root",passwd="",host="localhost",db="coba")
cursor = con.cursor()

def has_dup(StoreData):
    sd = StoreData
    unique = []
    hs = []
    for i in range(0, len(sd)-1):    
        hs.extend([sd.iloc[i,4]])

    a = []
    index = -1
    for i in hs:
        j = []
        index += 1
        if len(i.split(' ')) > 2 :
            for z in i.split(' '):
                #print(z)
                j.append(z)
                print(j)
            hs[index] = (i.split(' '))[0]   
        a.extend(j)
    #print(a)
    hs.extend(a)
    print(hs)
    
    
    for hashtag in hs: 
            if hashtag not in unique: 
                unique.append(hashtag) 
            #return unique
        #print(sd.iloc[i,4])
    #print(unique)

"""
def masuk_hashtag(StoreData):
    sd = StoreData
    sql = "INSERT INTO hashtag(isi) VALUES ( %s )"
    #for i in range(0, len(sd)-1):
    
        #print(sd.iloc[i,4])
        #cursor.execute(sql,(
        #    sd.iloc[i,4])
        #)

    #con.commit()
    
    #cursor.close()
    #con.close()
   
def masuk_db(StoreData):

    sd = StoreData
    sql = "INSERT INTO tweet(tweet, Username, RT, SA) VALUES (%s,%s,%s,%s)"
    #print(sd.iloc[:,1])
    for i in range(0,len(sd)-1):
        cursor.execute(sql.format( 
        
        sd.iloc[i,3],
        sd.iloc[i,1], 
        sd.iloc[i,5], 
        sd.iloc[i,7]))
        
        con.commit()
    
    cursor.close()
    con.close()
"""