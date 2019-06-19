import json
import pandas as pd
import networkx as nx
import matplotlib.cm as cmm
import matplotlib.pyplot as plt
from pandas import Timestamp
import numpy as np
from datetime import date, datetime
from twython import Twython
from Lib.create_db import input_database 
#import Lib.create_db
from Lib.GrafGenerator import Grap_Generate as gg

class SENTET:

    def login_twitter(CONSUMER_KEY='qXVo3PXRvaxRDinwEqluagyGB', CONSUMER_SECRET='8vkWXs30seGMJeJ21tg5SXXY0Lry9kdYhvJEGS3mYXIE6LHHpp', 
        ACCESS_TOKEN='1707115609-D1axGwQkv2Mn2NOXd1sHqZbnQx0DqIJoHANI26V', ACCESS_SECRET='liUdv7bkjUAWB347pl4oPfjhwlsHdzlAOn9fee6MoFhGL'):
        key = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
        return key

    def pencarian(cari, key):
        from Lib.NLP import NLP 
        twitter = key
        NLP = NLP()
        getminedata = NLP.MineData(twitter, cari ,2)
        dp = NLP.ProsesStoreData(getminedata)
        df = NLP.ProcessSentiment(getminedata)
        dfs = NLP.ProcessHashtags(getminedata)
        dft = NLP.ProcessTimestamp(getminedata)
        
        """
        Proses Memasukan Data ke dalam Database sql
        """
        ID = input_database()
        ID.masuk_tweet(dp[1]) #tabel tweet
        ID.masuk_retweet(dp[0]) #tabel retweet
        #ID.sambungan(dp[1]) #tabel_cari

        #Export Grap dari Class Grap_Generate
        #gg.Word(dp)
        return(dp) 