import pandas as pd
import sqlite3
import pandas.io.sql 
import numpy as np
from pandas import Timestamp
from datetime import datetime

import pymysql
pymysql.install_as_MySQLdb() 
import MySQLdb


pymysql.converters.encoders[Timestamp] = pymysql.converters.escape_datetime
pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.encoders[np.int64] = pymysql.converters._escape_table
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

con = MySQLdb.connect(user="root",passwd="",host="localhost",db="coba3")
cursor = con.cursor(pymysql.cursors.DictCursor)

def table_tweet(StoreData):
    
    sd = StoreData
    for a in range(0,len(sd)-1):
            
            sql2 = "INSERT INTO `tweet` (`id`, `Username`, `tanggal`, `tweet`, `hashtag`, `RT`, `SA`, `SAP`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

            cursor.execute(sql2,(

            sd.iloc[a,0],        
            sd.iloc[a,1],
            sd.iloc[a,2], 
            sd.iloc[a,3], 
            sd.iloc[a,4],
            sd.iloc[a,5],
            sd.iloc[a,6],
            sd.iloc[a,7]))
            
            con.commit()

    close_cursor()

def close_cursor():    
    cursor.close()
    con.close()
