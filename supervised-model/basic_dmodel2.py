#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 12:14:24 2025

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import csv

class Model:
    def __init__(self):
        self.model = keras.models.Sequential()
        self.model.add(keras.Input(shape=(2, 10)))
        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(30, kernel_initializer='he_normal', 
                                            activation=keras.layers.LeakyReLU(negative_slope=0.01), use_bias=False))
        self.model.add(keras.layers.Dense(30, kernel_initializer='he_normal', 
                                            activation='sigmoid', use_bias=False))
        self.model.add(keras.layers.Dense(30, kernel_initializer='he_normal', 
                                            activation=keras.layers.LeakyReLU(negative_slope=0.01), use_bias=False))
        self.model.add(keras.layers.Dense(19, activation="softmax", 
                                            use_bias=False))
        self.optimizer = keras.optimizers.Adam(learning_rate=0.001)
        
        self.moves = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0",
                      "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]
    
    def model_play(self, current_move, scenario_no):
        with tf.GradientTape() as tape:
            # Make a move
            probabilities = self.model(current_move, training=True)

            move_index = tf.argmax(probabilities, axis=1)
            move_probability = tf.reduce_max(probabilities, axis=1)

            # Convert scenario_no-1 to tensor and expand dimensions
            scenario_no_tensor = tf.convert_to_tensor([scenario_no-1], dtype=tf.int64)

            # Get the loss
            loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=scenario_no_tensor, logits=probabilities)


        # Calculate the gradients
        grads = tape.gradient(loss, self.model.trainable_weights)

        # Update the model
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_weights))
        # Convert input to tensor if it's not already
        current_move = tf.convert_to_tensor(current_move, dtype=tf.float32)

        # Get model probabilities
        probabilities = self.model(current_move, training=False)
        
        # Get the selected action
        action = self.moves[int(move_index)]
        print(action)
        return action