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
from fungsi_db import *

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

        #print(float(sd.iloc[a,5]))
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
                        SELECT `idT` FROM `tweet` WHERE `tweet` = %s;
                        """
                        cursor.execute(sqlhs, sd.iloc[a,3]) #check idT 
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
                        
                    #print('ooop')
        else :
            #print('JAANCOOK')
            pass
##### PASS

def masuk_retweet(StoreData):

    sdr = StoreData
    #print(sdr)
    for a in range(0,len(sdr)-1):
        sqlt = """
        SELECT `idR` FROM `retweet` WHERE `idJsonR` = %s; 
        """
        cursor.execute(sqlt, sdr.iloc[a,1])
        hasilt = cursor.fetchall()
        print("hasil retweet sama = ", len(hasilt))
        if len(hasilt) > 0:    
            pass
        else: 
           
            input_retweet(sdr, a, hasilt) 
        
            sqlcari = """
            SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s; 
            """ 
            cursor.execute(sqlcari, sdr.iloc[a,0])
            hascari = cursor.fetchall()
            print("idJsonT sama = ", len(hascari))
            if len(hascari) > 0:
                pass
            else:
                input_rt_t(sdr,a)
        
        sqlint = """
        SELECT `idT` FROM `tweet` WHERE idJsonT = %s;
        """

        cursor.execute(sqlint, sdr.iloc[a,0])
        hasint = cursor.fetchall()
        #print(hasint)

        input_retweet(sdr, a, hasint)
                
            
            #print('ooop')
        
##### PASS
                        
def sambungan(StoreData):
    sd = StoreData
    
    for a in range(0,len(sd)-1):
        
        #print(float(sd.iloc[a,5]))
        x = sd.iloc[a,4].split(" ") #displit
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
                        SELECT `idT` FROM `tweet` WHERE idJsonT  = %s;
                        """
                        cursor.execute(sqlhs, sd.iloc[a,0]) #check idT 
                        hs = cursor.fetchall()
                        print("tweet sama = ", len(hs)) 

                        if len(hs) > 0:
                            input_sambungan(hast, hs)
                        else :
                            input_tweet(sd, a)
                        
                        sqlin = """
                        SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s
                        """

                        cursor.execute(sqlin, a)
                        hsi = cursor.fetchall()

                        print(hsi)
            
                    else :
                                     
                        sqlhas = """
                        INSERT INTO `hashtag` (`isi`) VALUES (%s)
                        """ 
                    #    cursor.execute(sqlhas, i)
                    #    hasts = cursor.fetchall()
                    #    con.commit()
                            
                        sqlin = """
                        SELECT `idT` FROM `tweet` WHERE `idJsonT` = %s
                        """
                    #    cursor.execute(sqlin, sd.iloc[a,0])
                    #    hstgl = cursor.fetchall()
                        #print(len(hstgl))

                        #if len(hstgl) > 0: #bila ada
                        #    pass 
                        #else :
                    #        input_tweet(sd, a)
                        #    pass
                        #print(has) = ()
                        
                    #print('ooop')
        else :
            #print('JAANCOOK')
            pass
##### PASS

def close_cursor():    
    cursor.close()
    con.close()
