from SENTET import NLP

cari = '2019GantiPresiden'

dataaccum = NLP.MineData(twitter, cari ,2)

#print(dataaccum)

dp = (NLP.ProsesStoreData(dataaccum))
df = NLP.ProcessSentiment(dataaccum)
dfs = NLP.ProcessHashtags(dataaccum)
dft = NLP.ProcessTimestamp(dataaccum)