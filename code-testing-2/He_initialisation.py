#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 16:46:05 2024

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
from keras import layers
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

#He initialisation using fan_avg rather than fan_in
he_avg_init = keras.initializers.VarianceScaling(scale=2., mode='fan_avg',
                                                     distribution='uniform')
#to implement, below let kernel_initializer=he_avg_init

input_ = layers.Input(shape=X_train.shape[1:])
#layers are called like a function, passing it the input_ layer
#hence the name functional API
hidden1 = layers.Dense(30, activation="relu", kernel_initializer="he_normal")(input_)
hidden2 = layers.Dense(30, activation="relu", kernel_initializer="he_normal")(hidden1)
concat = layers.Concatenate()([input_, hidden2])
output = layers.Dense(1)(concat)
model = keras.Model(inputs=[input_], outputs=[output])

model.compile(loss="mse", optimizer=keras.optimizers.SGD(learning_rate=1e-3), metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=20,
                    validation_data=(X_valid, y_valid))
mse_test = model.evaluate(X_test, y_test)
X_new = X_test[:3] #pretend these are new instances
y_pred = model.predict(X_new)


print(y_pred)

y_new = y_test[:3]
print(y_new) #shows the answer










