#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:42:34 2024

@author: theahellen
"""

import tensorflow as tf
import numpy as np
from tensorflow import keras
from scikeras.wrappers import KerasClassifier, KerasRegressor
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from scipy.stats import reciprocal
from sklearn.model_selection import RandomizedSearchCV


def build_model(n_hidden=1, n_neurons=30, lr=3e-3, input_shape=[8]):
    model = keras.models.Sequential() 
    model.add(keras.layers.InputLayer(input_shape=input_shape))
    for layer in range(n_hidden): 
        model.add(keras.layers.Dense(n_neurons, activation="relu"))
    model.add(keras.layers.Dense(1))
    optimizer = keras.optimizers.SGD(learning_rate=lr)
    model.compile(loss="mse", optimizer=optimizer)
    return model

keras_reg = KerasRegressor(build_model)

housing = fetch_california_housing()

X_train_full, X_test, y_train_full, y_test = train_test_split(
    housing.data, housing.target)
X_train, X_valid, y_train, y_valid = train_test_split(
    X_train_full, y_train_full)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)
X_test = scaler.transform(X_test)
X_new = X_test[:3]

keras_reg.fit(X_train, y_train, epochs=10,
              validation_data=(X_valid, y_valid),
              callbacks=[keras.callbacks.EarlyStopping(patience=10)])
mse_test = keras_reg.score(X_test, y_test)
y_pred = keras_reg.predict(X_new)


#something wrong with this
param_distribs = {
        "n_hidden": [0, 1, 2, 3],
        "n_neurons": list(range(1, 100)),
        "lr": [1/3e-4, 1/3e-2],
}
    
rnd_search_cv = RandomizedSearchCV(keras_reg, param_distribs, n_iter=10, cv=3)
    
rnd_search_cv.fit(X_train, y_train, epochs=10,
                      validation_data=(X_valid, y_valid),
                      callbacks=[keras.callbacks.EarlyStopping(patience=10)])

print(rnd_search_cv.best_params_)
print(rnd_search_cv.best_score_)

model = rnd_search_cv.best_estimator_.model
model.save("hyperparameter_tuning_random.keras")



