from keras.models import Sequential, load_model
from keras.layers import Dense
import numpy

# Обучаем нейросеть

dataset = numpy.loadtxt("DATASET.csv", delimiter=";")
# разбиваем датасет на матрицу параметров (X) и вектор целевой переменной (Y)
X, Y = dataset[:, 1:31], dataset[:, 0:1]

model = Sequential()
model.add(Dense(30, input_dim=30, activation='sigmoid')) # входной слой требует задать input_dim
model.add(Dense(15, activation='sigmoid'))
model.add(Dense(8, activation='sigmoid'))
model.add(Dense(15, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid')) # сигмоида вместо relu для определения вероятности

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])

model.fit(X, Y, epochs=1000, batch_size=100)
model.save("C:\\andrew\\projects\\netology\\model")

scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
