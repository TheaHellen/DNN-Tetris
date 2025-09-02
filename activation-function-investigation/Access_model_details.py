#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:01:49 2025

@author: theahellen
"""

import tensorflow as tf

def load_and_print_weights(model_path):
    # Load the saved Keras model
    model = tf.keras.models.load_model(model_path)
    
    # Iterate through each layer and print its weights and biases
    for layer in model.layers:
        print(f"Layer: {layer.name}")
        weights = layer.get_weights()
        if weights:  # Check if the layer has weights
            for i in range(0, len(weights), 2):
                print(f"  Weights shape: {weights[i].shape}")
                print(weights[i])  # Print weight values
                if i + 1 < len(weights):  # Check if there are biases
                    print(f"  Biases shape: {weights[i+1].shape}")
                    print(weights[i+1])  # Print bias values
        else:
            print("  No trainable weights in this layer.")
        print("-" * 50)

# Example usage
model_path = "/Users/theahellen/Documents/Uni/Year 4/Dissertation/tetris-diss/backpropagation-by-hand/model.keras"  # Replace with your actual model path
load_and_print_weights(model_path)