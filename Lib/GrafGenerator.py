from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pandas as pd
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import numpy as np

"""
Class Grap_Generate berfungsi untuk meng-export 
data yang telah dicrawl sebelumnya menjadi :
Grap Batang (Total hashtag)
Grap PieChart (Sentiment Analysis)
WordCloud
dan Node
"""

class Grap_Generate:
        
    def PieChart(StoreData):
          
        pos_tweet = StoreData['SA'].value_counts()

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

    def Graf(SentimentData, HashtagData, TimestampData):

        df = SentimentData

        df = df.astype({'Polarity': 'float64'})

        SentimentbyDate = df.groupby([df['Date'].dt.date, 
                                df['Date'].dt.hour, 
                                df['Date'].dt.minute])['Polarity'].mean()
        df = TimestampData

        TwittbyDate = df.groupby([df['Date'].dt.date, 
                                df['Date'].dt.hour, 
                                df['Date'].dt.minute]).size()
        df = HashtagData
        
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

    def Word(StoreData):

        dp = StoreData
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

    def Node(StoreData):

        G = nx.Graph()
        G.clear()
        dp = StoreData

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

        plt.savefig("export/node.png", format='PNG')
        nx.write_gexf(G, "node-hashtag.gexf")
        print("Node Telah Diexport")
