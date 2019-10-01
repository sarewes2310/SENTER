![alt text](https://raw.githubusercontent.com/Sarewes2310/SENTET/master/static/asset/Logo/senter.png?token=AVp8RroIPfI2JxAkhoiin7WnAQvqSRycks5cZA6qwA%3D%3D)
<br><br>
SENTER adalah sebuah RESTful API yang berguna untuk menganalisa sebuah kalimat. Kalimat akan di kelompokan menjadi tiga kriteria, yaitu: postif, negatif, netral 
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
5. Pastikan ada flask
6. Enjoy

### Usage 

1. langsung run file ```template.py```
2. buka browser url : ```127.0.0.1:5000```

# API
1. JSON graf network ```127.0.0.1:5000/ujiTampilan/json ```
2. Get All Data berdasarkan pencaharian ```127.0.0.1:5000/getApiAll```
