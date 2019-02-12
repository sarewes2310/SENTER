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
from .fungsi_db import *
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

"""
Class yang berfungsi menginputkan data dari DataFrame ke Database SQL
Mengunakan Pymysql AS MySQLdb

terdiri dari 4 tabel : tweet, retweet, hashtag, tabel_cari
*file (DB/sentiment_analysis_twitter-2.sql)

Proses peng-inputan ke database melalui beberapa iterasi 'SELECT',
untuk mencegah redudansi data.

"""

class input_database :
        
    def masuk_tweet(StoreData):

        sd = StoreData
        
        for a in range(0,len(sd)-1):
            sqlt = """
            SELECT `idT` FROM `tweet` WHERE `tweet` = %s
            """
            cursor.execute(sqlt, sd.iloc[a,3])
            hasilt = cursor.fetchall()
            print("hasil tweet sama = ", len(hasilt))
            if len(hasilt) > 0:
                pass
            else:
                input_tweet(sd, a)

            x = sd.iloc[a,4].split(" ") #displit
            if len(x) > 2: #dicheck apabila jumlah isi > 2
                
                for i in x:
                    if i is not '': #dicheck sisa pembagian dari split  
                        sqlh = """
                        SELECT `idH` FROM `hashtag` WHERE `isi` = %s;
                        """            
                        cursor.execute(sqlh, i)
                        hast = cursor.fetchall()
                        
                        print("hast sama = ", len(hast))
                        
                        if len(hast) > 0: # jika data > 0
                            #for e in sd.iloc[a,3]: #tweet
                            sqlhs = """
                            SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s;
                            """
                            cursor.execute(sqlhs, sd.iloc[a,0]) #check idT 
                            hs = cursor.fetchall()
                            print("tweet sama = ", len(hs)) 
                            
                        else :
                                        
                            sqlhas = """
                            INSERT INTO `hashtag` (`isi`) VALUES (%s)
                            """ 
                            cursor.execute(sqlhas, i)
                            hasts = cursor.fetchall()
                            con.commit()
                                
                            sqlin = """
                            SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s
                            """
                            cursor.execute(sqlin, sd.iloc[a,0])
                            hstgl = cursor.fetchall()
                            #print(len(hstgl))

                            if len(hstgl) > 0: #bila ada
                                pass 
                            else :
                                input_tweet(sd, a)
                            #print(has) = ()

            else :
                pass
    ##### PASS

    def masuk_retweet(StoreData):

        sdr = StoreData
        #print(sdr)
        for a in range(0,len(sdr)-1):
            sqlt = """
            SELECT `idR` FROM `retweet` WHERE `idJsonR` = %s; 
            """
            print(sdr.iloc[a,1])
            cursor.execute(sqlt, sdr.iloc[a,1])
            hasilt = cursor.fetchall()
            print("hasil retweet sama = ", len(hasilt))
            if len(hasilt) > 0:    
                pass
            else: 
            
            #    input_retweet(sdr, a, hasilt) 
            
                sqlcari = """
                SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s; 
                """ 
                cursor.execute(sqlcari, sdr.iloc[a,0]['id_str'])
                hascari = cursor.fetchall()

                if len(hascari) > 0:
                    sqltc = """
                    SELECT `idR` FROM `retweet` WHERE `idJsonR` = %s; 
                    """
                    cursor.execute(sqltc, sdr.iloc[a,1])
                    haschk = cursor.fetchall()
                    if len(haschk) > 0:
                    #    print(len(haschk))
                        pass 
                    else:
                        ##TO DO : - Check Hashtag;

                        x = sdr.iloc[a,5].split(" ") #displit
                        if len(x) > 2: #dicheck apabila jumlah isi > 2
                            
                            for i in x:
                                if i is not '': #dicheck sisa pembagian dari split  
                                    sqlh = """
                                    SELECT `idH` FROM `hashtag` WHERE `isi` = %s;
                                    """            
                                    cursor.execute(sqlh, i)
                                    hast = cursor.fetchall()
                                    
                                    print("hast sama = ", len(hast))
                                    
                                    if len(hast) > 0: # jika data > 0
                                        
                                        sqlhs = """
                                        SELECT `idT` FROM `tweet` WHERE `tweet` = %s;
                                        """
                                        cursor.execute(sqlhs, sdr.iloc[a,0]['id']) #check idT 
                                        hsrtb = cursor.fetchall()
                                        #print("tweet sama = ", len(hsrtb)) 
                                        
                                    else :
                                                    
                                        sqlhas = """
                                        INSERT INTO `hashtag` (`isi`) VALUES (%s)
                                        """ 
                                        cursor.execute(sqlhas, i)
                                        con.commit()

                                        sqlhs = """
                                        SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s;
                                        """
                                        cursor.execute(sqlhs, sdr.iloc[a,0]['id']) #check idT 
                                        hsrtb = cursor.fetchall()
                                        #print("tweet sama = ", len(hsrtb))
                                        if len(hsrtb) > 0 :
                                                
                                            sqlin = """
                                            SELECT `idR` FROM `retweet` WHERE `idJsonR` = %s
                                            """
                                            cursor.execute(sqlin, sdr.iloc[a,1])
                                            hstglrtb = cursor.fetchall()
                                            #print(len(hstgl))

                                            if len(hstglrtb) > 0: #bila ada
                                                pass 
                                            else :
                                                input_retweet(sdr, a, hsrtb)
                                                con.commit()
                                        else :
                                            input_rt_t(sdr, a)

                                            sqlin = """
                                            SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s;
                                            """
                                            cursor.execute(sqlhs, sdr.iloc[a,0]['id'])
                                            hstglrtbin = cursor.fetchall()

                                            input_retweet(sdr, a, hstglrtbin)
                                            con.commit()
                                            
                                        #print(has) = ()

                                else :
                                    pass
                        #input_retweet(sdr, a, hascari)

                else:
                    
                    input_rt_t(sdr,a)
                    con.commit()
            
                    sqlint = """
                    SELECT `idT` FROM `tweet` WHERE `idJsonT` = '%s'
                    """
                    #print(sdr.iloc[a,0])
                    cursor.execute(sqlint, sdr.iloc[a, 0]['id'])
                    hasint = cursor.fetchall()
                    #print("ini retweet ke 2 : ",sdr.iloc[a,0]['id_str']," == ", hasint )
                    
                    print(hasint)
                    sqltck = """
                    SELECT `idR` FROM `retweet` WHERE `idJsonR` = %s; 
                    """
                    cursor.execute(sqltck, sdr.iloc[a,1])
                    cursor.fetchall() 
                    #######
                    # Bug :
                    # See -> https://github.com/PyMySQL/PyMySQL/issues/399
                    #######
                    haschek = cursor.fetchall()
                    #print(haschek)
                    if len(haschek) > 0:
                        pass 
                    else:
                        input_retweet(sdr, a, hasint)
                
            
    ##### PASS
                            
    def sambungan(StoreData):
        sds = StoreData
        
        for a in range(0,len(sds)-1):
            
            x = sds.iloc[a,4].split(" ") #displit
            if len(x) > 2: #dicheck apabila jumlah isi > 2
                
                for i in x:
                    if i is not '': #dicheck sisa pembagian dari split  
                        sqlh = """
                        SELECT `idH` FROM `hashtag` WHERE `isi` = %s;
                        """            
                        cursor.execute(sqlh, i)
                        hast = cursor.fetchall()
                        
                        print("hast sama = ", hast)
                        #print(x)
                        
                        if len(hast) > 0: # jika data > 0
                            
                            sqlhs = """
                            SELECT `idT` FROM `tweet` WHERE `idJsonT`  = %s;
                            """
                            cursor.execute(sqlhs, sds.iloc[a,0]) #check idT 
                            hs = cursor.fetchall()
                            print("tweet sama = ", len(hs)) 

                            if len(hs) > 0:
                                input_sambungan(hs, hast) #(IDtweet, IDhashtag)
                                #cursor.fetchall()
                                con.commit()
                            else :
                                input_tweet(sds, a)
                                con.commit()

                                sqlinb = """
                                SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s;
                                """
                                #print("========= BUG =========")
                                #print(sds.iloc[a,0])
                                cursor.execute(sqlinb, sds.iloc[a,0])
                                print(cursor.fetchall())
                                #######
                                # Bug :
                                # See -> https://github.com/PyMySQL/PyMySQL/issues/399
                                # fix : double con.commit()
                                #######
                                cursor.execute(sqlinb, sds.iloc[a,0])
                                hsb = cursor.fetchall()
                                print(hsb)
                                input_sambungan(hsb, hast)
                                
                
                        else :
                                        
                            sqlhas = """
                            INSERT INTO `hashtag` (`isi`) VALUES (%s)
                            """ 
                            cursor.execute(sqlhas, i)
                            con.commit()
                                
                            sqlin = """
                            SELECT `idH` FROM `hashtag` WHERE `isi` = %s
                            """
                            cursor.execute(sqlin, i)
                            hastg = cursor.fetchall()
                            #print(len(hstgl))
                            
                            sqlst = """
                            SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s
                            """

                            cursor.execute(sqlst, sds.iloc[a,0])
                            hasst = cursor.fetchall()

                            if len(hasst) > 0:
                                input_sambungan(hasst, hastg)
                            else:
                                input_tweet(sds, a)

                                sqlsl = """
                                SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s
                                """
                                cursor.execute(sqlst, sds.iloc[a,0])
                                hasstb = cursor.fetchall()

                                input_sambungan(hasstb, hastg)
                        
            else :
                pass
    ##### PASS
    def cari_tanggal():
        sqltang = "SELECT * FROM `tweet` WHERE `tanggal` >= %s"
        ms = input("YYYY-MM-DD : ")
        cursor.execute(sqltang, ms)
        msa = cursor.fetchall()
        print(msa)

    def close_cursor():    
        cursor.close()
        con.close()