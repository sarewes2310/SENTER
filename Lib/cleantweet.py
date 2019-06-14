import re,string
import nltk
import csv
import numpy as np 

""""
Class clean tweet berfungsi sebagai
normalisasi dataset yang akan di training,
dengan cara regex, dan mengganti kata slang 
di tweet berdasarkan KBBI (data/kbba.txt) dan rootword (data/rootword.txt)

kedua file tersebut dapat di update secara manual
"""

class CleanTweet:
	KATA_DASAR  = []
	DATA_KBBI 	= []

	def __init__(self):
		global KATA_DASAR
		global DATA_KBBI
		KATA_DASAR 	= [line.strip('\n')for line in open('Lib/data/rootword.txt')]
		DATA_KBBI	= [kamus.strip('\n').strip('\r') for kamus in open('Lib/data/kbba.txt')]

	def tokenize(self, tweet): 
		# token = nltk.word_tokenize(tweet)
		""" Fungsi yang digunakan untuk membagi kalimat menjadi kata"""
		token = tweet.split(' ')
		return token

	def kbbi(self, token): 
		""" Fungsi yang digunakan untuk """
		global DATA_KBBI
		#ubah list menjadi dictionary 
		dic = {}
		for i in DATA_KBBI: 
			(key,val) = i.split('\t')
			dic[str(key)] = val
		#kbbi cocokan 
		final_string = ' '.join(str(dic.get(word, word)) for word in token).split()
		return final_string

	def normalize_token(self, _tokens):
		tokens = self.kbbi(_tokens)
		return tokens
	
	def hapus_tanda(self, tweet): 
		tanda_baca = set(string.punctuation)
		tweet = ''.join(ch for ch in tweet if ch not in tanda_baca)
		return tweet

	def hapus_katadouble(self, s): 
	    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
	    return pattern.sub(r"\1\1", s)

	def preprocess(self, tweet):
		tweet = tweet.lower()
		tweet = re.sub(r'\\u\w\w\w\w', '', tweet)
		tweet = re.sub(r'http\S+','',tweet) #hapus link
		tweet = re.sub('@[^\s]+','',tweet) #hapus @username
		tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #hapus #tagger 
		tweet = self.hapus_tanda(tweet) #hapus tanda baca
		tweet = re.sub(r'\w*\d\w*', '',tweet).strip() #hapus angka dan angka yang berada dalam string 
		tweet = self.hapus_katadouble(tweet) #hapus repetisi karakter 
		return tweet

	def prep(self, sent):
		return self.normalize_token(self.tokenize(self.preprocess(sent)))

	def clean_text_tweet(self, tweet):
		print(tweet)
		tweet = re.sub(r'\\u\w\w\w\w', '', tweet)
		tweet = re.sub(r'http\S+','',tweet) #hapus link
		#tweet = re.sub(r'RT','',tweet)
		tweet = re.sub('@[^\s]+','',tweet) #hapus username
		tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #hapus tagger
		tweet = re.sub(r'\w*\d\w*', '',tweet).strip() #hapus angka & str(angka)
		tweet = self.hapus_katadouble(tweet) #lurus
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())