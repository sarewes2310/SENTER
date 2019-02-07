from analiser import Analiser
from os import path

an = Analiser(training_data='data/coba_train.csv')

# load model
filename = 'model'
an.load_model(filename)

kata1 = input("Pos > " )

print (kata1)
print (an.testFromTrained([an.tfidf_data.transform(kata1)]))

kata2 = input("Neg > ")
print (kata2)
print (an.testFromTrained([an.tfidf_data.transform(kata2)]))
