#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 15:20:06 2024

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras


#%% CREATING THE MODEL USING SEQUENTIAL API
#downloads the data
fashion_mnist = keras.datasets.fashion_mnist

#data is already split into a training and a test set
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

print(X_train_full.shape)
print(X_train_full.dtype)

#scaling the pixel intesity (0-255) to 0-1 instead
X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]

class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", 
               "Sneaker", "Bag", "Ankle boot"]

#the first image in the training set represents a coat
print(class_names[y_train[0]])

#creating a sequential model
model = keras.models.Sequential()

#first layer: converts each image (28x28 array) to a 1d array
#specify the shape of the instances to see the model summary and save the model
model.add(keras.layers.Flatten(input_shape=[28, 28]))

#dense layers
model.add(keras.layers.Dense(300, activation="relu"))
model.add(keras.layers.Dense(100, activation="relu"))

#output layer
model.add(keras.layers.Dense(10, activation="softmax"))

#rather than writing keras.layers can write: from tensorflow.keras import layers
#then write model.add(layers.Dense(....))

#also, rather than writing model.add each line you can write the following:
'''
model = keras.models.Sequential([
    keras.layers.Flatten(input_shape=[28, 28]),
    keras.layers.Dense(300, activation="relu"),
    keras.layers.Dense(100, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
    ])
'''

print(model.summary())

#prints a list of the models layers
print(model.layers)
#you can fetch a layer by index
hidden1 = model.layers[1]
#you can print its name
print(hidden1.name)
#and fetch by its name
#print(model.get_layer('dense') is hidden1) #outputs True

#you can access the paramters of a layer like so
weights, biases = hidden1.get_weights()
print(weights)
print(weights.shape)
print(biases)
print(biases.shape)

#%% COMPILING THE MDOEL

model.compile(loss="sparse_categorical_crossentropy",
              optimizer="sgd",
              metrics=["accuracy"])
#"sgd" means we are training the model using stochastic gradient descent
#in general, you want to tune the learning rate, do this by writing:
#optimizer=keras.optimizers.SGD(lr=...)
#default is lr=0.01

#since this is a classifier its useful to measure accuracy

#%% TRAINING AND EVALUATING THE MODEL

#fit the model
history = model.fit(X_train, y_train, epochs=30, 
                    validation_data=(X_valid, y_valid))

import pandas as pd
import matplotlib.pyplot as plt

# Create a DataFrame
df = pd.DataFrame(history.history)

# Create a figure with a higher dpi
plt.figure(figsize=(8, 5), dpi=300)  # Set the figure size and dpi
df.plot(ax=plt.gca())  # Plot on the current axes
plt.grid(True)
plt.gca().set_ylim(0, 1)  # Set the vertical range to [0,1]
plt.gca().set_xlim(0, 30)  # Set the horizontal range to [0,30]

# Show the plot
plt.show()

#evaluate the model
model.evaluate(X_test, y_test)

#%% USING THE MODEL TO MAKE PREDICTIONS

X_new = X_test[:3]
print(type(X_new))
y_proba = model.predict(X_new) #predicts the probability of each class
print(y_proba.round(2))

import numpy as np
y_pred = np.argmax(y_proba, axis=1) #predicts the class with prob 1 or 0
print(y_pred)
print(np.array(class_names)[y_pred])

y_new = y_test[:3]
print(y_new) #shows the answer: its the same

#%% SAVING THE MODEL

model.save("model_A.h5")
















