#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 18:21:37 2024

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras

fashion_mnist = keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", 
               "Sneaker", "Bag", "Ankle boot"]

#remove sandal and shirt from the database
X_train_full, X_test = X_train_full / 255.0, X_test / 255.0

sandal_class = 5  
shirt_class = 6   

train_mask = (y_train_full != sandal_class) & (y_train_full != shirt_class)
test_mask = (y_test != sandal_class) & (y_test != shirt_class)

X_train_B = X_train_full[train_mask]
y_train_B = y_train_full[train_mask]

X_valid_B, X_train_B = X_train_B[:5000], X_train_B[5000:]
y_valid_B, y_train_B = y_train_B[:5000], y_train_B[5000:]

X_test_B = X_test[test_mask]
y_test_B = y_test[test_mask]


#load model A
model_A = keras.models.load_model("../chap10_code_testing/model_A.h5")

model_A_clone = keras.models.clone_model(model_A)
model_A_clone.set_weights(model_A.get_weights())

model_B_on_A = keras.models.Sequential(model_A.layers[:-1])
model_B_on_A.add(keras.layers.Dense(1, activation="sigmoid"))

for layer in model_B_on_A.layers[:-1]: 
    layer.trainable = False
    
model_B_on_A.compile(loss="binary_crossentropy", optimizer="sgd",
                         metrics=["accuracy"])

history = model_B_on_A.fit(X_train_B, y_train_B, epochs=4,
                               validation_data=(X_valid_B, y_valid_B))
for layer in model_B_on_A.layers[:-1]: 
    layer.trainable = True
optimizer = keras.optimizers.SGD(learning_rate=1e-4) # the default lr is 1e-2 
model_B_on_A.compile(loss="binary_crossentropy", optimizer=optimizer,
                         metrics=["accuracy"])
history = model_B_on_A.fit(X_train_B, y_train_B, epochs=16,
                               validation_data=(X_valid_B, y_valid_B))

print(model_B_on_A.evaluate(X_test_B, y_test_B))