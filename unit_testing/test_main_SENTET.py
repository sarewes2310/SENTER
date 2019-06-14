from Lib.SENTET import NLP
from Lib.TwitterConfig import *
from Lib.create_db import input_database as ID
from Lib.GrafGenerator import Grap_Generate as gg


########
#Contoh Pengunaan
########
twitter = login()
NLP = NLP()

cari = 'NurhadiAldo'

dataaccum = NLP.MineData(twitter, cari ,2)

#print(dataaccum)

dp = NLP.ProsesStoreData(dataaccum)
df = NLP.ProcessSentiment(dataaccum)
dfs = NLP.ProcessHashtags(dataaccum)
dft = NLP.ProcessTimestamp(dataaccum)

print("===================================================================== \n")

#Proses Memasukan Data ke dalam Database sql


ID.masuk_tweet(dp[1]) #tabel tweet
ID.masuk_retweet(dp[0]) #tabel retweet
ID.sambungan(dp[1]) #tabel_cari


#Export Grap dari Class Grap_Generate


#gg.PieChart(dp)
#gg.Graf(df, dfs, dft)
gg.Word(dp)
#gg.Node(dp)
