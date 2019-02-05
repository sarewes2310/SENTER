from analiser import Analiser
from os import path


an = Analiser(training_data='data/coba_train.csv')

# train new model
filename='model'
an.train(filename)

kata1 = input("Pos > " )

print (kata1)
ap = an.testFromTrained([an.tfidf_data.transform(kata1)])
print(ap)

kata2 = input(" Neg > ")
print (kata2)
ap = an.testFromTrained([an.tfidf_data.transform(kata2)])
print(ap)
