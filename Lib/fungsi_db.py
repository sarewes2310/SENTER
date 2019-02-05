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


def input_iter_tweet(sd, a):
    sqli = """
    INSERT INTO `tweet` 
    (`IdJsonT`, `tweet`, `tanggal`, `Username`, `RT`, `SA`) 
    VALUES (%s, %s, %s, %s, %s, %s);"""

    for a in range(0,len(sd)-1):     
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
    
    for rowI in hasrtj:                         
        
        #print(i['idT'])
        #a = i['idT']
        cursor.execute(sqli,(

        rowI['idT'],      #idT
        sdr.iloc[a,1],  #IDRetweet 
        sdr.iloc[a,3], #Tanggal
        sdr.iloc[a,2], #Username
        sdr.iloc[a,4], #Retweet
        sdr.iloc[a,6], #RT
        sdr.iloc[a,7]))#SA "pos, net, neg
        
        con.commit()


def input_iter_retweet(sd):
    sqli = """
    INSERT INTO `tweet` 
    (`idT`, `idJsonR`, `tweet`, `tanggal`, `Username`, `RT`, `SA`) 
    VALUES (%s, %s, %s, %s, %s, %s);"""

    for a in range(0,len(sd)-1):     
        cursor.execute(sqli,(

        hasrti,
        sd.iloc[a,0], #ID tweet
        sd.iloc[a,3], #tweet
        sd.iloc[a,2], #Date
        sd.iloc[a,1], #User
#        sd.iloc[a,5], #Retweet Count
        sd.iloc[a,6]))#SA "pos, net, neg"
        
        con.commit()

def input_rt_t(sdr, a):
        sqli = """
        INSERT INTO `tweet` 
        (`idJsonT`, `tweet`, `tanggal`, `Username`, `RT`, `SA`)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sqli,(
        sdr.iloc[a,0], #ID tweet
        sdr.iloc[a,4], #tweet
        sdr.iloc[a,3], #Date
        sdr.iloc[a,2], #User
        sdr.iloc[a,6], #Retweet Count
        sdr.iloc[a,7]))#SA "pos, net, neg"

        con.commit()
        
def input_sambungan(hast, hs):

        sqli = """
        INSERT INTO `tabel_cari` 
        (`idT`, `idH`)
        VALUES (%s, %s)
        """
        #print(hast[0]['idH'])
        #print(hs[0]['idT'])

        cursor.execute(sqli,(
        hs[0]['idT'], # ID twitter 
        hast[0]['idH'] # ID hashtag
        

        ))
        con.commit()