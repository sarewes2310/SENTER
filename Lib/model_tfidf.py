from __future__ import division
import string
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from .cleantweet import CleanTweet
import os

"""
Class TFID berfungsi sebagai pembobotan (pemberial value) pada kata
berdasarkan rumus TF - IDF (Term Frequency - Index Document Fequency) 
"""
class TFIDF:
	all_data = []
	onlyX	 = []

	# asumsi korpus terdiri dari array panjang 2, 
	# indeks 0 -> array xdata
	# indeks 1 -> array ydata
	# asumsi panjang indeks 0 dan indeks 1 sama
	def __init__(self, corpus):
		self.preprocessor = CleanTweet()
		self.tfidf_vectorizer = self.initVectorizer()
		self.tfidf_data = self.tfidf_vectorizer.fit_transform(corpus[0])
		self.fitData(corpus[1])

	"""
	Fungsi iniVectorizer berguna sebagai parameter
	awal sebelum dataset olah, format data hampir sama 
	dengan word2vec
	"""
	def initVectorizer(self):
		tokenize = lambda sent: self.preprocessor.prep(sent)
		return TfidfVectorizer(
			norm='l2',
			min_df=0,
			#stop_words='data/stopword.txt', :: coba == fail
			max_features=1000,
			use_idf=True, 
			smooth_idf=False, 
			sublinear_tf=True, 
			tokenizer=tokenize
		)

	"""
	Fungsi yang digunakan untuk menggabungkan array dengan index semua data
	"""
	def fitData(self, ydata):
		i = 0
		self.all_data = []
		for count_0, doc in enumerate(self.tfidf_data.toarray()):
			self.onlyX.append(doc)
			self.all_data.append([doc, ydata[i]])
			i += 1

	def transform(self, sent):
		return self.tfidf_vectorizer.transform([sent]).toarray()[0]

	"""
	Fungsi yang dipakai untuk mengambil semua data sentiment dan data text training
	"""
	def getData(self):
		return self.all_data


	"""
	Fungsi yang digunakan hanya untuk mengambil data sentiment training
	"""
	def getOnlyX(self):
		return self.onlyX