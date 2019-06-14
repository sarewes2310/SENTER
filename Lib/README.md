
"""
Main Program yang berfungsi mencrawl data twitter 
dan menjadikan 2 data besar Tweet dan Retweet 

Note: model dapat ditraining, atau di-load, atau di retrain 

an = Analiser(training_data='data/coba_train.csv')

#Training :
filename='model'
an.train(filename)

#Load:
filename = 'model'
an.load_model(filename)

#Retrain:
filename = 'model'
an.retrain(filename)

#Contoh Print Hasil Sentimen :
kata1 = input() 
print (an.testFromTrained([an.tfidf_data.transform(kata1)])) #float
print (an.testFromTrained([an.tfidf_data.transform(kata2)])) #Pos, Net, Neg


########
#Contoh Pengunaan
########

cari = 'NurhadiAldo'

NLP = NLP()
dataaccum = NLP.MineData(twitter, cari ,2)

#print(dataaccum)

dp = NLP.ProsesStoreData(dataaccum)
df = NLP.ProcessSentiment(dataaccum)
dfs = NLP.ProcessHashtags(dataaccum)
dft = NLP.ProcessTimestamp(dataaccum)

print("===================================================================== \n")

#Proses Memasukan Data ke dalam Database sql

from create_db import input_database as ID

ID.masuk_tweet(dp[1]) #tabel tweet
ID.masuk_retweet(dp[0]) #tabel retweet
ID.sambungan(dp[1]) #tabel_cari

#Export Grap dari Class Grap_Generate

#from GrafGenerator import Grap_Generate

#gg = Grap_Generate
#gg.PieChart(dp)
#gg.Graf(df, dfs, dft)
#gg.Word(dp)
#gg.Node(dp)
"""

#twitter = login() #load TwitterConfig 

#Memanggil Class Analiser untuk load data set