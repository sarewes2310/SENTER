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

""" Library SENTET """
#from .fungsi_db import *
from .cleantweet import CleanTweet #cuma import fungsi clean_tweet()
from .analiser import Analiser

import pymysql
pymysql.install_as_MySQLdb() 
import MySQLdb

pymysql.converters.encoders[Timestamp] = pymysql.converters.escape_datetime
pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.encoders[np.int64] = pymysql.converters._escape_table
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

con = MySQLdb.connect(user="root",passwd="",host="localhost",db="cobasentimentanalysis")
cursor = con.cursor(pymysql.cursors.DictCursor)

"""
Class yang berfungsi menginputkan data dari DataFrame ke Database SQL
Mengunakan Pymysql AS MySQLdb

terdiri dari 4 tabel : tweet, retweet, hashtag, tabel_cari
*file (DB/sentiment_analysis_twitter-2.sql)

Proses peng-inputan ke database melalui beberapa iterasi 'SELECT',
untuk mencegah redudansi data.

"""
class input_database:
    CT = CleanTweet()
    ##### DONE #####
    def select_network(self, cari):
        print("hds")
        sqln = """
        SELECT * FROM `tag_trigger` INNER JOIN `hashtag` ON `tag_trigger.idH` = `hashtag.idH` INNER JOIN `tweet` ON `tag_trigger.idT` = `tweet.idT` 
        """
        cursor.execute(sqln)
        hasiln = cursor.fetchall()        
        return hasiln

    ##### DONE #####
    def select_tweet(self):
        print("hds")
        sqlt = """
        SELECT * FROM `tweet`
        """
        cursor.execute(sqlt)
        hasilt = cursor.fetchall()        
        return hasilt

    ##### DONE #####
    def select_retweet(self):
        print("hds")
        sqlrt = """
        SELECT * FROM `retweet`
        """
        cursor.execute(sqlrt)
        hasilrt = cursor.fetchall()        
        return hasilrt

    ##### DONE #####
    def select_tweet_date(self,cari_from,cari_to):
        print("hds")
        sqlt = """
        SELECT * FROM `tweet` WHERE `tanggal` >= %s AND `tanggal` <= %s
        """
        cursor.execute(sqlt,(cari_from,cari_to))
        hasilt = cursor.fetchall()        
        return hasilt

    ##### DONE #####
    def select_retweet_date(self,cari_from,cari_to):
        print("hds")
        sqlrt = """
        SELECT * FROM `retweet` WHERE `tanggal` >= %s AND `tanggal` <= %s
        """
        cursor.execute(sqlrt,(cari_from,cari_to))
        hasilrt = cursor.fetchall()        
        return hasilrt

    ##### DONE #####
    def search_tweet(self,id_t):
        sqlt = """
        SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s
        """
        cursor.execute(sqlt, id_t)
        hasilt = cursor.fetchall()
        return hasilt

    ##### DONE #####
    def search_hashtag(self,id_h):
        sqlh = """
        SELECT `idH` FROM `hashtag` WHERE `isi` = %s;
        """            
        cursor.execute(sqlh, id_h)
        hasilhast = cursor.fetchall()
        return hasilhast

    ##### DONE #####
    def search_retweet(self,id_rt):
        sqlt = """
        SELECT `idR` FROM `retweet` WHERE `idJsonR` = %s; 
        """
        #print(sdr.iloc[a,1])
        cursor.execute(sqlt, id_rt)
        hasilrt = cursor.fetchall()
        #print("hasil retweet sama = ", len(hasilt))
        return hasilrt

    ##### DONE #####
    def input_tweet(self,sd):
        sqli = """
        INSERT INTO `tweet` 
        (`idJsonT`, `tweet`, `tanggal`, `Username`, `RT`, `SA`) 
        VALUES (%s, %s, %s, %s, %s, %s);"""
        cursor.execute(sqli,(
            sd[0], #ID tweet
            sd[1], #tweet
            sd[2], #Date
            sd[3], #User
            sd[4], #Retweet Count
            sd[5]) #SA "pos, net, neg"
        )
        con.commit()

    ##### DONE #####
    def input_retweet(self,sdr):
        sqli = """
        INSERT INTO `retweet` 
        (`idT`, `idJsonR`, `tanggal`, `Username`, `retweet`, `RT`, `SA`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        #print(i['idT'])
        #a = i['idT']
        cursor.execute(sqli,(
            sdr[0],  #idT
            sdr[1],  #IDRetweet 
            sdr[2], #Tanggal
            sdr[3], #Username
            sdr[4], #Retweet
            sdr[5], #RT
            sdr[6]) #SA "pos, net, neg
        )
        con.commit()

    ##### DONE #####
    def input_hashtag(self,sdh):
        sql = """
        INSERT INTO `hashtag` (`isi`) VALUES (%s)
        """ 
        cursor.execute(sql, sdh)
        hasts = cursor.fetchall()
        con.commit()
        return hasts

    ##### TESTING #####
    def input_rt_t(self,sdr, a):
        sqli = """
        INSERT INTO `tweet` 
        (`idJsonT`, `tweet`, `tanggal`, `Username`, `RT`, `SA`)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        #print(sdr.iloc[a,0]['id'])
        cursor.execute(sqli,(
            str(sdr.iloc[a,0]['id']), #ID tweet
            CT.clean_text_tweet((sdr.iloc[a,0])['full_text']), #tweet
            sdr.iloc[a,0]['created_at'], #Date
            sdr.iloc[a,0]['user']['screen_name'], #User
            sdr.iloc[a,0]['retweet_count'], #Retweet Count
            sdr.iloc[a,7]) #SA "pos, net, neg"
        )
        con.commit()
            
    ##### DONE #####
    def input_trigger(self,hs, hast): #(IDtweet, IDhashtag)
        sqli = """
        INSERT INTO `tag_trigger` 
        (`idT`, `idH`)
        VALUES (%s, %s)
        """
        cursor.execute(sqli, (
        hs, # ID twitter 
        hast)) #ID Hashtag    
        return con.commit()

    ##### DONE #####
    def masuk_tweet(self, StoreData):
        sd = StoreData  
        for a in range(0,len(sd)-1):
            id_jsont = sd.iloc[a,0]
            hasilt = self.search_tweet(id_jsont)
            if len(hasilt) == 0:
                data_tweet = [id_jsont,sd.iloc[a,3],sd.iloc[a,2],sd.iloc[a,1],sd.iloc[a,5],sd.iloc[a,6]]
                self.input_tweet(data_tweet) ##TO DO : - Input Tweet;
                x = sd.iloc[a,4].split(" ") #displit
                if len(x) > 2: #dicheck apabila jumlah isi > 2
                    for i in x:
                        if i is not '': #dicheck sisa pembagian dari split  
                            hast = self.search_hashtag(i)
                            if len(hast) == 0: # jika data == 0
                                self.input_hashtag(i)
                                hast = self.search_hashtag(i)
                            hasilt = self.search_tweet(id_jsont)
                            print(hasilt)
                            print(hast)
                            return self.input_trigger(int(hasilt[0]['idT']),int(hast[0]['idH'])) ##TO DO : - Insert Tag Trigger;
        return 0

    ##### TESTING #####
    def masuk_retweet(self, StoreData):
        sdr = StoreData
        print("RUNNN FUNCTION masuk_retweet")
        from Lib.NLP import NLP #memanggil library NLP 
        NLP.an = Analiser(training_data='Lib/data/coba_train.csv')
        filename = 'model'
        NLP.an.load_model(filename)
        for a in range(0,len(sdr)-1):
            id_jsonrt = sdr.iloc[a,1]
            id_jsont = sdr.iloc[a,0]['id_str']
            hasilt = self.search_retweet(id_jsonrt)
            ##TO DO : - Check Retweet;
            if len(hasilt) == 0:    
                tweetcari = self.search_tweet(id_jsont)
                ##TO DO : - Check Tweet;
                if len(tweetcari) > 0:
                    ##TO DO : - Check Hashtag;
                    x = sdr.iloc[a,5].split(" ") #displit
                    if len(x) > 2: #dicheck apabila jumlah isi > 2
                        for i in x:
                            if i is not '': #dicheck sisa pembagian dari split  
                                #sqlh = """
                                #SELECT `idH` FROM `hashtag` WHERE xisi` = %s;
                                #"""            
                                #cursor.execute(sqlh, i)
                                #hast = cursor.fetchall()
                                #print("hast sama = ", len(hast))
                                hast = self.search_hashtag(i)
                                if len(hast) == 0: # jika data > 0
                                    self.input_hashtag(i)
                                    hast = self.search_hashtag(i)
                                #tweetcari = self.search_tweet(id_jsont)
                                data_retweet = [tweetcari[0]['idT'],sdr.iloc[a,1],sdr.iloc[a,3],sdr.iloc[a,2],
                                sdr.iloc[a,4],sdr.iloc[a,6],sdr.iloc[a,7]]
                                self.input_retweet(data_retweet)
                                self.input_trigger(int(tweetcari[0]['idT']),int(hast[0]['idH']))
                    #input_retweet(sdr, a, hascari)
                else:
                    ##TO DO : - Check Hashtag;
                    print("RUNNN FUNCTION !!!!!")
                    x = sdr.iloc[a,5].split(" ") #displit
                    if len(x) > 2: #dicheck apabila jumlah isi > 2
                        for i in x:
                            if i is not '': #dicheck sisa pembagian dari split  
                                hast = self.search_hashtag(i)
                                if len(hast) == 0: # jika data > 0
                                    self.input_hashtag(i)
                                    hast = self.search_hashtag(i)
                                value_training = [NLP.an.tfidf_data.transform(sdr.iloc[a,0]['full_text'])]
                                data_tweet = [id_jsont,sdr.iloc[a,0]['full_text'],pd.to_datetime(sdr.iloc[a,0]['created_at']),
                                sdr.iloc[a,0]['user']['screen_name'],sdr.iloc[a,0]['retweet_count'],NLP.an.testStrFromTrained(value_training)]
                                self.input_tweet(data_tweet)
                                tweetcari = self.search_tweet(id_jsont)
                                data_retweet = [tweetcari[0]['idT'],sdr.iloc[a,1],sdr.iloc[a,3],sdr.iloc[a,2],
                                sdr.iloc[a,4],sdr.iloc[a,6],sdr.iloc[a,7]]
                                self.input_retweet(data_retweet)
                                self.input_trigger(int(tweetcari[0]['idT']),int(hast[0]['idH']))
                #######
                # Bug :
                # See -> https://github.com/PyMySQL/PyMySQL/issues/399
                #######
        return 0
    
    def cari_tanggal():
        sqltang = "SELECT * FROM `tweet` WHERE `tanggal` >= %s"
        ms = input("YYYY-MM-DD : ")
        cursor.execute(sqltang, ms)
        msa = cursor.fetchall()
        print(msa)

    def close_cursor():    
        cursor.close()
        con.close() 