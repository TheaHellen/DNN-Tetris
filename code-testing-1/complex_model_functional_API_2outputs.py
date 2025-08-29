#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 17:41:13 2024

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


input_A = layers.Input(shape=[5], name="wide_input")
input_B = layers.Input(shape=[6], name="deep_input")
hidden1 = layers.Dense(30, activation="relu")(input_B)
hidden2 = layers.Dense(30, activation="relu")(hidden1)
concat = layers.concatenate([input_A, hidden2])
output = layers.Dense(1, name="main_output")(concat)
aux_output = layers.Dense(1, name="aux_output")(hidden2)
model = keras.Model(inputs=[input_A, input_B], outputs=[output, aux_output])

model.compile(loss=["mse", "mse"], loss_weights=[0.9, 0.1],
              optimizer=keras.optimizers.SGD(learning_rate=1e-3))

X_train_A, X_train_B = X_train[:,:5], X_train[:,2:]
X_valid_A, X_valid_B = X_valid[:,:5], X_valid[:,2:]
X_test_A, X_test_B = X_test[:,:5], X_test[:,2:]
X_new_A, X_new_B = X_test_A[:3], X_test_B[:3]

#%% fitting the model

history = model.fit([X_train_A, X_train_B], [y_train, y_train], epochs=20,
                    validation_data=([X_valid_A, X_valid_B], [y_valid, y_valid]))
total_loss, main_loss, aux_loss = model.evaluate((X_test_A, X_test_B), y_test)

y_pred_main, y_pred_aux = model.predict((X_new_A, X_new_B))


print(y_pred_main, y_pred_aux)

y_new = y_test[:3]
print(y_new) #shows the answer

#%% HOW TO SAVE AND RESTORE A MODEL

model.save("keras_model_functionalAPI_2outputs.keras") #to save

model = keras.models.load_model("keras_model_functionalAPI_2outputs.keras") #to load

#this only works with sequential or functional API, not subclassing
#you can use save_weights() and load_weights() for subclassing, but have to do
#everything else manually

#%% USING CALLBACKS

#sometimes we want to save a model at regular checkpoints as it might take a while
#to train. to do this we can use callbacks

#build and compile model as above

#an example of what it would look like for a simple model
'''
checkpoint_cb = keras.callbacks.ModelCheckpoint("keras_model_functionalAPI_2outputs.h5")
history = model.fit(X_train, y_train, epochs=20, callbacks=[checkpoint_cb])
'''

#what to use if you use validation sets
#it will only save your model when its performance on the validation set is 
#the best so far

'''
checkpoint_cb = keras.callbacks.ModelCheckpoint("keras_model_functionalAPI_2outputs.keras",
                                                save_best_only=True)
history = model.fit([X_train_A, X_train_B], [y_train, y_train], epochs=20,
                    validation_data=([X_valid_A, X_valid_B], [y_valid, y_valid]), 
                    callbacks=[checkpoint_cb])
model = keras.models.load_model("keras_model_functionalAPI_2outputs.keras")
'''

#you can stop training early if there is no more progress

checkpoint_cb = keras.callbacks.ModelCheckpoint("keras_model_functionalAPI_2outputs.keras",
                                                save_best_only=True)

early_stopping_cb = keras.callbacks.EarlyStopping(patience=10,
                                                      restore_best_weights=True)

history = model.fit([X_train_A, X_train_B], [y_train, y_train], epochs=100,
                    validation_data=([X_valid_A, X_valid_B], [y_valid, y_valid]), 
                    callbacks=[checkpoint_cb, early_stopping_cb])

model = keras.models.load_model("keras_model_functionalAPI_2outputs.keras")
















