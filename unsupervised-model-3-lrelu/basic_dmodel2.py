#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 12:14:24 2025

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import LeakyReLU
import numpy as np
import csv

from Dgrid import Grid

class Model:
    def __init__(self):
        
        self.model = keras.models.Sequential()
        self.model.add(keras.Input(shape=(5, 10)))
        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(30, kernel_initializer='he_normal', 
                                            activation=keras.layers.LeakyReLU(negative_slope=0.01), use_bias=False))
        self.model.add(keras.layers.Dense(30, kernel_initializer='he_normal', 
                                            activation=keras.layers.LeakyReLU(negative_slope=0.01), use_bias=False))
        self.model.add(keras.layers.Dense(30, kernel_initializer='he_normal', 
                                            activation=keras.layers.LeakyReLU(negative_slope=0.01), use_bias=False))
        self.model.add(keras.layers.Dense(19, activation="softmax", 
                                            use_bias=False))
        self.optimizer = keras.optimizers.Adam(learning_rate=0.0008)
        
        self.moves = ["v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0",
                      "h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9"]
        
        self.current_grid = []
        
        self.row = 0
        self.gap = 0
        
        self.previous_action = "v1"

        self.count = 0

    
    def model_play(self, current_move, game_no, game_score):
        self.count += 1
        print(self.count)

        # # Adjust learning rate every 100,000 moves
        # if self.count % 1000 == 0:
        #     current_lr = self.optimizer.learning_rate.numpy()
        #     new_lr = current_lr * 0.9
        #     self.optimizer.learning_rate.assign(new_lr)
        #     print(f"Updated learning rate to: {new_lr}")

        # Convert input to tensor
        current_move = tf.convert_to_tensor(current_move, dtype=tf.float32)
        
        self.current_grid = current_move
        
        with tf.GradientTape() as tape:
            # Get model predictions
            probabilities = self.model(current_move, training=True)
            
            # Sample action from probabilities
            #log_probs = tf.math.log(probabilities)
            #action_index = tf.random.categorical(log_probs, 1)[0][0]
            
            # Remove the random element to check by hand
            action_index = np.argmax(probabilities)
            
            # Get the selected action
            action = self.moves[int(action_index)]
            
            # Calculate loss
            loss, grid_after_action, score = self.loss_fn(current_move, probabilities, action_index, action)
            
        # Calculate gradients
        grads = tape.gradient(loss, self.model.trainable_variables)
        
        # Apply gradients
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

        # Set current move as previous move for future use
        self.previous_action = action
        
        # Save to CSV
        self.save_to_csv(action, self.row, self.gap, loss, game_no, game_score)
        
        return action, grid_after_action, score
    

    def loss_fn(self, current_move, probabilities, action_index, action):
        # Get the number of the row the block will be placed in
        self.row = self.calculate_row_placement(action)

        # Get the probability of the chosen action
        action_prob = probabilities[0, action_index]
        
        # Punish for the row the block is placed in (squared)
        # Values ranging 1 to 25
        base_loss = self.row**2 
        
        # Punish if the model makes the same move twice
        # Values ranging 0 to 10
        repeat_loss = 0
        if self.previous_action == action:
            repeat_loss = 10
            
        # Reward for an increase in score
        # Values ranging 0 to 800 depending on the number of lines cleared
        score_loss = 0
        grid_instance = Grid()
        predicted_grid = current_move.numpy().flatten()
        predicted_grid = predicted_grid.reshape(5, 10)
        # Apply the chosen action to the grid
        if action[0] == "v":
            if int(action[1]) > 0:
                predicted_grid[5-self.row, int(action[1])-1] = 1
                predicted_grid[5-self.row-1, int(action[1])-1] = 1
            if int(action[1]) == 0:
                predicted_grid[5-self.row, 9] = 1
                predicted_grid[5-self.row-1, 9] = 1
        if action[0] == "h":
            predicted_grid[5-self.row, int(action[1])-1] = 1
            predicted_grid[5-self.row, int(action[1])] = 1
        # Set the grid to the predicted grid
        grid_instance.set_grid(predicted_grid)
        # Get the number of lines cleared
        lines_cleared = 0
        lines_cleared = grid_instance.clear_full_rows()
        # Calculate the score loss
        if lines_cleared == 1:
            score_loss = 100
        if lines_cleared == 2:
            score_loss = 300
        if lines_cleared == 3:
            score_loss = 500
        if lines_cleared == 4:
            score_loss = 800
        
        # Punish for leaving any gaps
        # Values ranging 0 to 64
        self.gap = self.calculate_gap(action)
        gap_loss = self.gap**3 

        # Reward for vertical moves (higher reward for row 1)
        # Values ranging 25 to 50
        if action[0] == "v":
            v_loss = 25
            if self.row == 1:
                v_loss = 50 
        else:
            v_loss = 0

        # Punish for losing a game
        # Values ranging 0 to 100
        game_loss = 0
        if action[0] == "v" and self.row >=4:
            game_loss = 100
        if action[0] == "h" and self.row == 5:
            game_loss = 100

        # Punish is -, reward is +
        return (-base_loss + action_prob/100000 - repeat_loss + score_loss - 
                 gap_loss + v_loss - game_loss), grid_instance.grid, score_loss

        #return (-base_loss + action_prob/100000 + score_loss), grid_instance.grid, score_loss

    
    def calculate_row_placement(self, action):
        # 1 1
        if action[0] == "h":
            col = int(action[1])
            col -= 1 # Zero based indexing
            
            row = 4
            while self.current_grid[0, 5-row, col] == 0 and self.current_grid[0, 5-row, col+1] == 0:
                row -= 1
                if row == 0:
                    break
            
        # 1
        # 1
        if action[0] == "v":
            col = int(action[1])
            if col == 0:
                col = 10
            col -=1 # Zero based indexing
            
            row = 4
            while self.current_grid[0, 5-row, col] == 0 and self.current_grid[0, 5-row-1, col] == 0:
                row -= 1
                if row == 0:
                    break
                
        return row+1
    

    def calculate_gap(self, action):
        gap = 0
        row = self.row-1
        col = int(action[1])
        col -= 1 # Zero based indexing
        
        if action[0] == "h" and row!=0:
            while self.current_grid[0, 5-row, col] == 0 or self.current_grid[0, 5-row, col+1] == 0:
                row -= 1
                gap += 1
                if row == 0:
                    break
                
                
        
        return gap

            

    def save_to_csv(self, action, no_rows, gap, loss, no_games, score):
        filename = "log-lrelulrelusig-lr0005.csv"
        
        file_exists = False
        try:
            with open(filename, 'r'):
                file_exists = True
        except FileNotFoundError:
            pass
        
        if not file_exists:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['move', 'row placement', 'gap left', 
                                 'loss', 'score', 'game no.'])
        
        row = [action, no_rows, gap, loss.numpy(), 
               score, no_games]
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

        # Save the model
        model_filename = "model-lrelulrelusig-lr0005.keras"
        self.model.save(model_filename)