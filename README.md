![alt text](https://raw.githubusercontent.com/Sarewes2310/SENTET/master/static/asset/Logo/SENTET_2.png?token=AVp8RroIPfI2JxAkhoiin7WnAQvqSRycks5cZA6qwA%3D%3D)
<br><br>
SENTET adalah sebuah RESTful API yang berguna untuk menganalisa sebuah tweet yang berkaitan dengan pemilu. Tweet akan di kelompokan menjadi tiga kriteria, yaitu: postif, negatif, netral dengan ekstraksi fitur TF-IDF 
# Getting Started
Buat terlebih dahulu api pada halaman developer twitter https://apps.twitter.com. Registrasi aplikasi yang telah anda buat.
Setelah berhasil simpan ```Consumer Key```, ```Consumer Secret```, ```Api Key ```, dan ```Api Secret Key``` yang didapat tab Apps.
Kemudian isikan di file TwitterConfig.py

### Prerequisites
Dalam menggunakan RESTful API SENTET memerlukan beberapa library tambahan:
```
twython, pandas, matplotlib, numpy, keras, tensorflow, scikit-learn, nltk, networkx, plotly, pymyql
```

### Instalation

1. ```git clone https://github.com/Sarewes2310/SENTET.git ``` atau download zip via web
2. Isikan ```Consumer Key```, ```Consumer Secret```, ```Api Key ```, dan ```Api Secret Key``` pada TwitterConfig.py
3. Buat Database SQL, file database terdapat pada folder ```DB/sentiment_analysis_twitter-2.sql``` 
4. Buat Model dengan cara run python file di folder ```test/test_main_training.py```
5. Enjoy

### Usage 

# Train / Pre-Trained

```python
an = Analiser(training_data='data/coba_train.csv')

# train model baru
filename='model'
an.train(filename)

kata1 = input("Pos > " )
ap = an.testFromTrained([an.tfidf_data.transform(kata1)])
print(ap)

#re-train
filename = 'model'
an.retrain(filename)

kata1 = input("Pos > " )

print (kata1)
print (an.testFromTrained([an.tfidf_data.transform(kata1)]))

#load model
filename = 'model'
an.load_model(filename)

kata1 = input("Pos > " )

print (kata1)
print (an.testFromTrained([an.tfidf_data.transform(kata1)]))
```

# API
sdasda
