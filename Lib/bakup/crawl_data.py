from twython import Twython
import time
import collections
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from TwitterConfig import *
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sqlalchemy import create_engine
#import pymysql

#dialect+driver://username:password@host:port/database
#engine = create_engine('mysql://root:@localhost:8800/sentimen', echo=False)

#from cleantweet import CleanTweet as CT

from analiser import Analiser

twitter = login()

an = Analiser(training_data='data/coba_train.csv')

# load model
filename='model'
an.load_model(filename)

def MineData(apiobj, query, pagestocollect = 10):

    results = apiobj.search(q=query, include_entities='true',
                            tweet_mode='extended',count='450',
                            result_type='recent')

    data = results['statuses']
    i=0
    ratelimit=1
    
    while results['statuses'] and i<pagestocollect: 
        
        if ratelimit < 1: 
            print(str(ratelimit)+'Rate limit!')
            break
        
        mid= results['statuses'][len(results['statuses']) -1]['id']-1

        print(mid)
        print('Panjang status : '+str(len(results['statuses'])))
        
        results = apiobj.search(q=query, max_id=str(mid)
                            ,include_entities='true',
                            tweet_mode='extended',count='450',
                            result_type='recent')
        
        data+=results['statuses']
        i+=1
        ratelimit = int(apiobj.get_lastfunction_header('x-rate-limit-remaining'))

    return data

def ProcessHashtags(data):
    HashtagData = pd.DataFrame(columns=['HT','ID','Date','RAWDATA_INDEX'])
    
    for index,twit in enumerate(data):
        HashtagData = HashtagData.append(pd.DataFrame({'ID':twit['id'],
                        'Date':pd.to_datetime(twit['created_at']),
                        'RAWDATA_INDEX':index,
                        'HT':[hashtag['text'] for hashtag 
                                in twit['entities']['hashtags']]})
                            , ignore_index=True)

    return HashtagData

def ProcessTimestamp(data):
    TimestampData = pd.DataFrame(columns=['ID','Date','RAWDATA_INDEX'])
    
    for index,twit in enumerate(data):
        TimestampData = TimestampData.append(pd.DataFrame({'ID':[twit['id']],
                        'Date':[pd.to_datetime(twit['created_at'])],
                        'RAWDATA_INDEX':[index]})
                            , ignore_index=True)

    return TimestampData

def clean_tweet(tweet):   
    
    def hapus_katadouble(s):
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return  pattern.sub(r"\1\1", s)
    
    #tweet=tweet.lower()
    tweet = re.sub(r'\\u\w\w\w\w', '', tweet)
    tweet = re.sub(r'http\S+','',tweet)# hapus link
    tweet = re.sub(r'RT','',tweet)
    tweet = re.sub('@[^\s]+','',tweet)# hapus username
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)# hapus tagger
    tweet=re.sub(r'\w*\d\w*', '',tweet).strip() #hapus angka & str(angka) 
    tweet=hapus_katadouble(tweet) # lurus
    
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())



def ProcessSentiment(data):
    SentimentData = pd.DataFrame(columns=['ID','Date','Polarity'], dtype = float)
    
    for index,twit in enumerate(data):
        SentimentData = SentimentData.append(pd.DataFrame({'ID':[twit['id']],
                        'Date':[pd.to_datetime(twit['created_at'])],
                        'Polarity':[an.testFromTrained([an.tfidf_data.transform(twit['full_text'])])]})
                            , ignore_index=True)

    return SentimentData

def ProsesStoreData(data):
    StoreData = pd.DataFrame(columns=['ID', 'Username', 'Date', 'Tweet', 'Hashtags', 'RT', 'SA', 'Float'], dtype=float).fillna('0')

    for index, twit in enumerate(data):
        a = ''
        for hashtag in twit['entities']['hashtags']:
            if hashtag['text'] is None:
                a = ' '
            else:
                a = a + str(hashtag['text'] + '; ')

        StoreData = StoreData.append(pd.DataFrame({
                    'ID':[twit['id']],
                    'Username':[twit['user']['screen_name']],
                    'Date':[twit['created_at']],
                    'Tweet':[clean_tweet(twit['full_text'])],
                    'Hashtags':[a],
                    'RT':[twit['retweet_count']],
                    'SA':[an.testStrFromTrained([an.tfidf_data.transform(twit['full_text'])])],
                    'Float':[an.testFromTrained([an.tfidf_data.transform(twit['full_text'])])]
                    }))

    StoreData.to_csv('export/out.csv')

    #StoreData.to_sql('sentimen', con=engine)
    #engine.execute("SELECT * FROM sentimen").fetchall()

    return StoreData

cari = input('Masukan Kata Kunci > ')
dataaccum = MineData(twitter, cari, 20)

#Menampilkan Graf Sentimen
dp =  ProsesStoreData(dataaccum)

pos_tweet = dp['SA'].value_counts()

colors = ['yellowgreen','gray','lightcoral']
pos_tweet.plot.pie(
           shadow=False,
           colors=colors, 
           explode=(0.1, 0.1, 0.1),
           startangle=90,
           autopct='%1.1f%%'
           )

plt.tight_layout()
plt.savefig('export/test_graph_pie.png', dpi = 96)
print("Graph Pie Chart Telah Diexport")
plt.gcf().clear()


df = ProcessSentiment(dataaccum)
df = df.astype({'Polarity': 'float64'})

SentimentbyDate = df.groupby([df['Date'].dt.date, 
                        df['Date'].dt.hour, 
                        df['Date'].dt.minute])['Polarity'].mean()

ProcessTimestamp(dataaccum)   

TwittbyDate = df.groupby([df['Date'].dt.date, 
                        df['Date'].dt.hour, 
                        df['Date'].dt.minute]).size()

df =  ProcessHashtags(dataaccum)

hashtagCountData = df['HT'].value_counts()

x = np.arange(TwittbyDate.size)

fit = np.polyfit(x, TwittbyDate, 1)
fit_fn = np.poly1d(fit)
#Plot data
TwittbyDate.plot()
plt.plot(x, fit_fn(x), 'r-')
plt.plot(x, TwittbyDate, 'g-', ms=4)
plt.xticks(rotation=90)

plt.xlabel('Tanggal, Jam, Menit')
plt.ylabel('Twitter disebut per menit')
plt.legend(["NLP Sentiment Polarity antara 0 to 1",
            "Liner regression untuk rata - rata di mention"])
#plt.title("Query text: ")

ax2=plt.twinx()
ax2.set_ylim(0,1)

ColorMap = SentimentbyDate > 0
SentimentbyDate.plot.bar(color=ColorMap.map({True: 'b', False: 'r'}),ax=ax2 )

plt.ylabel('Sentimet polarity')
plt.tight_layout()

#plt.savefig('export/test_graph.png')
#print("Sentimen Graph Telah diexport")
plt.gcf().clear()

hashtagCountData.head(20).plot.bar()
plt.tight_layout()

#Save hashtag data plot 
plt.savefig('export/test_graph_hashtag.png')
print("Hastags graph telah diexport")
plt.gcf().clear()

# Save WordCloud Image
dp =  ProsesStoreData(dataaccum)

text = " ".join(txt for txt in dp['Tweet'])

stopwords = set(STOPWORDS)
custom = open('data/stopword.txt', 'r', encoding='utf-8').readlines()
stopwords.update(custom)

wordcloud = WordCloud(height=1080, stopwords=stopwords, width=1920, background_color="white").generate(text)

plt.figure(figsize=(24, 12))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
#plt.show()
wordcloud.to_file("export/test_graph_wordclloud.png")
print("WordCloud telah diexport")
plt.gcf().clear()


import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
G = nx.Graph()
G.clear()

hashtags = []
for hash_list in dp.values[:,4]:
    hashtags.extend(hash_list[2:-2].split('; '))
from collections import OrderedDict
hashtags = list(OrderedDict.fromkeys(hashtags))
for hashtag in hashtags:
    G.add_node(hashtag.lower(), name=hashtag.lower())

edges = []
for hash_list in dp.values[:,4]:
    hash_list = hash_list[2:-2].split('; ')
    if len(hash_list) > 1:
        for i in range(0,len(hash_list)):
            for j in range(i+1,len(hash_list)):
                edges.append([hash_list[i].lower(), hash_list[j].lower()])
for edge in edges:
    G.add_edge(edge[0], edge[1])

G.remove_nodes_from([d[0] for d in G.degree if d[1] <= 10 ])

nx.draw(G, node_size=1600, cmap=plt.cm.Reds,
        node_color=range(len(G)), pos=nx.random_layout(G), with_labels=True)

#plt.savefig("Graph.png", format="PNG")
#plt.show()
plt.savefig("export/node.png", format='PNG')
nx.write_gexf(G, "node-hashtag.gexf")
print("Node Telah Diexport")

G1 = nx.Graf()
G1.clear()

dp.sort_value(["RT"], ascending=False)
dp_rt = dp.drop(dp[dp.RT <= 10].index)
dp_rt.sort_value(["RT"], ascending=False).head(10)
