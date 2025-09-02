#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 17:12:53 2025

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import csv

class Model:
    def __init__(self):
        #create a sequential model
        self.model = keras.models.Sequential()

        #input layer to define the input shape
        self.model.add(keras.Input(shape=(20, 10)))

        #convert each grid (20x10 array) to a 1D array
        self.model.add(keras.layers.Flatten())

        #dense layers
        self.model.add(keras.layers.Dense(200, kernel_initializer='RandomNormal', activation="relu"))
        self.model.add(keras.layers.Dense(100, kernel_initializer='RandomNormal', activation="relu"))
        self.model.add(keras.layers.Dense(100, kernel_initializer='RandomNormal', activation="relu"))

        #output layer
        self.model.add(keras.layers.Dense(19, activation="softmax"))
        
        self.hidden1 = self.model.layers[1]
        self.hidden2 = self.model.layers[2]
        self.hidden3 = self.model.layers[3]

        #print the weights of each layer
        '''
        weights, biases = self.hidden1.get_weights()
        print(weights)
        weights, biases = self.hidden2.get_weights()
        print(weights)
        weights, biases = self.hidden3.get_weights()
        print(weights)
        '''

        self.model.compile()
        
        self.moves = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9",
                      "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0"]
        
        self.optimizer = keras.optimizers.Adam(learning_rate=0.01)
        
    def random_model_play(self, current_move):
        next_move = self.model.predict(current_move)
        print(next_move)
        next_move = np.argmax(next_move, axis=1)
        
        return self.moves[next_move[0]]
    
    def loss_fn(self, current_move):
        #check if any element in each row is 1 (along axis 1)
        rows_with_one = tf.reduce_any(current_move == 1, axis=1)
        #count the number of rows that contain at least one 1
        self.no_rows = tf.reduce_sum(tf.cast(rows_with_one, tf.float32))
        return tf.constant(np.floor((self.no_rows-1.0)/2.0), dtype=tf.float32)
    
    def save_to_csv(self, current_move, action, no_rows):
        filename = "log_1.csv"
        
        file_exists = False
        try:
            with open(filename, 'r'):
                file_exists = True
        except FileNotFoundError:
            pass
        
        if not file_exists:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['grid', 'move', 'number of rows'])
        
        row = [current_move.numpy().flatten(), action, no_rows]
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        
    
    def model_play(self, current_move):
        with tf.GradientTape() as tape: #this allows calculations of the gradients
            probabilities = self.model(current_move)
            action_index = tf.random.categorical(tf.math.log(probabilities), 1)
            loss = self.loss_fn(current_move)
        #compute the gradients
        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        action = self.moves[action_index]
        self.save_to_csv(current_move, action, self.no_rows)
        return action
    
        








