#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 12:14:24 2025

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import LeakyReLU
import numpy as np
import csv

class Model:
    def __init__(self):
        #load model
        self.model = load_model("model-lrelusigsig-lr0005-batch-rewardnonrepeatedmoves.keras", custom_objects={'LeakyReLU': LeakyReLU})
        
        self.moves = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0",
                      "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]
        
        self.current_grid = []
    
    def model_play(self, current_move):
        # Convert input to tensor if it's not already
        current_move = tf.convert_to_tensor(current_move, dtype=tf.float32)
        
        self.current_grid = current_move

        # Get model probabilities
        probabilities = self.model(current_move, training=False)
        
        # Get the selected action
        action_index = np.argmax(probabilities)
        action = self.moves[int(action_index)]
        
        return action