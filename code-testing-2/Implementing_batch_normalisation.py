#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:23:50 2024

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

housing = fetch_california_housing()

X_train_full, X_test, y_train_full, y_test = train_test_split(
    housing.data, housing.target)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_train_full, y_train_full)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)
X_test = scaler.transform(X_test)

#to implement batch normalisation we add a BatchNormalisation layer before or
#after each hidden layer's activation function, and optionally a BN layer as the 
#first layer in the model

#this is us adding the BN layer AFTER the activation function
'''
model = keras.models.Sequential([
    keras.layers.BatchNormalization(),
    keras.layers.Dense(30, input_shape=X_train.shape[1:], activation="elu",
                       kernel_initializer="he_normal"),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(1)
    ])
'''

#to add the BN layer BEFORE the activation function (as recommended)

model = keras.models.Sequential([
        keras.layers.BatchNormalization(),
        keras.layers.Dense(30, input_shape=X_train.shape[1:], kernel_initializer="he_normal",
                           use_bias=False),
        keras.layers.BatchNormalization(),
        keras.layers.Activation("elu"),
        keras.layers.Dense(1)
])



model.compile(loss="mean_squared_error", optimizer="sgd", metrics=["accuracy"])


history = model.fit(X_train, y_train, epochs=20,
                    validation_data=(X_valid, y_valid))
mse_test = model.evaluate(X_test, y_test)
X_new = X_test[:3] #pretend these are new instances
y_pred = model.predict(X_new)

print(model.summary())
print([(var.name, var.trainable) for var in model.layers[1].variables])

print(y_pred)

y_new = y_test[:3]
print(y_new) #shows the answer