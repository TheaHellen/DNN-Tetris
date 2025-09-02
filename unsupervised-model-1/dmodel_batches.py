#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 14:45:46 2025

@author: theahellen
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import csv

class Model:
    def __init__(self, model_path=None):
        if model_path:
            # Load the pre-trained model
            self.model = keras.models.load_model(model_path)
        else:
            # Create a new sequential model
            self.model = keras.models.Sequential()

            # Input layer to define the input shape
            self.model.add(keras.Input(shape=(20, 10)))

            # Convert each grid (20x10 array) to a 1D array
            self.model.add(keras.layers.Flatten())

            # Dense layers with bias_initializer set to zeros
            self.model.add(keras.layers.Dense(100, kernel_initializer='RandomNormal', activation="sigmoid"))
            self.model.add(keras.layers.Dense(50, kernel_initializer='RandomNormal', activation="sigmoid"))
            self.model.add(keras.layers.Dense(50, kernel_initializer='RandomNormal', activation="sigmoid"))

            # Output layer with bias_initializer set to zeros
            self.model.add(keras.layers.Dense(19, activation="softmax"))

        self.hidden1 = self.model.layers[1]
        self.hidden2 = self.model.layers[2]
        self.hidden3 = self.model.layers[3]

        self.optimizer = keras.optimizers.Adam(learning_rate=0.3)
        
        self.moves = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9",
                     "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v0"]
        
        self.current_grid = []
        
        self.row = 0
        self.gap = 0
        
        self.previous_score = 0
        self.previous_game_no = 0
        self.previous_action = "h5"

        # Number of episodes to play before updating the model
        self.no_episodes = 1
        self.grads = []
        self.rewards = []
        self.all_rewards = []
        self.all_grads = []
        self.count = 0

        # Set discount factor
        self.discount_factor = 0.1
    
    def model_play(self, current_move, score, game_no):
        # Convert input to tensor if it's not already
        current_move = tf.convert_to_tensor(current_move, dtype=tf.float32)
        self.current_grid = current_move
        
        with tf.GradientTape() as tape:
            # Get model predictions
            probabilities = self.model(current_move, training=True)
            
            # Sample action from probabilities
            #log_probs = tf.math.log(probabilities)
            #action_index = tf.random.categorical(log_probs, 1)[0][0]

            # Get the selected action
            action_index = np.argmax(probabilities)
            action = self.moves[int(action_index)]
            
            # Calculate loss
            loss = self.loss_fn(current_move, probabilities, action_index, action, score)
            
        # Calculate gradients
        grads = tape.gradient(loss, self.model.trainable_variables)
        
        # Save the loss and the gradients then update the count
        self.rewards.append(loss)
        self.grads.append(grads)
        self.count += 1
        
        # Discount the rewards when the game ends
        if game_no != self.previous_game_no:
            self.all_rewards.extend(self.discount_rewards())
            self.all_grads.extend(self.grads)
            self.grads = []
            self.rewards = []

            # If we have played the required number of games update the model
            if game_no%self.no_episodes == 0 and game_no!=0:
                # Normalize rewards
                self.all_rewards = self.normalize_rewards(self.all_rewards)

                # Apply gradients
                for var_index, var in enumerate(self.model.trainable_variables):
                    mean_gradients = np.mean([self.all_grads[move][var_index] * self.all_rewards[move] for move in range(len(self.all_rewards))], axis=0)
                    self.optimizer = keras.optimizers.Adam(learning_rate=0.3)
                    self.optimizer.apply_gradients([(mean_gradients, var)])

                # Reset rewards
                self.all_rewards = []
                self.all_grads = []

                # Reset count
                self.count = 0
        
        # Get the selected action
        action = self.moves[int(action_index)]

        # Set current move as previous move for future use
        self.previous_action = action
        
        # Save to CSV
        self.save_to_csv(current_move, action, self.row, self.gap, loss, game_no, score, self.count)
        
        # Set the previous game number
        self.previous_game_no = game_no

        # Play selected action
        return action
    
    def loss_fn(self, current_move, probabilities, action_index, action, score):
        # Get the number of the row the block will be placed in
        self.row = self.calculate_row_placement(action)
        
        # Calculate base loss based on the row
        #base_loss = tf.floor((self.row-1.0)/2.0)
        
        # Calculate base loss as the squared row placement
        base_loss = self.row**2
        
        # Get the probability of the chosen action
        action_prob = probabilities[0, action_index]
        
        # If the model makes the same move twice - punish it
        repeat_loss = 0
        if self.previous_action == action:
            repeat_loss = 10
            
        # Reward for an increase in score - will also punish when the score 
        # decreases when a new game is initialised
        # So also punishes for losing the game
        score_change = score - self.previous_score
        self.previous_score = score
        
        # Punish for leaving any gaps
        self.gap = self.calculate_gap(action)
        gap_loss = self.gap**3

        return -(base_loss - action_prob/100000 + repeat_loss - score_change + gap_loss)

    def calculate_row_placement(self, action):
        # 1 1
        if action[0] == "h":
            col = int(action[1])
            col -= 1 # Zero based indexing
            
            row = 19
            while self.current_grid[0, 20-row, col] == 0 and self.current_grid[0, 20-row, col+1] == 0:
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
            
            row = 19
            while self.current_grid[0, 20-row, col] == 0 and self.current_grid[0, 20-row-1, col] == 0:
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
            while self.current_grid[0, 20-row, col] == 0 or self.current_grid[0, 20-row, col+1] == 0:
                row -= 1
                gap += 1
                if row == 0:
                    break
                
                
        
        return gap

            

    def save_to_csv(self, current_move, action, no_rows, gap, loss, no_games, score, count):
        filename = "log.csv"
        
        file_exists = False
        try:
            with open(filename, 'r'):
                file_exists = True
        except FileNotFoundError:
            pass
        
        if not file_exists:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['grid', 'move', 'row placement', 'gap left', 
                                 'loss', 'score', 'game no.', 'weights layer 1', 
                                 'weights layer 2', 'weights layer 3', 'count'])
        
        weights1 = self.hidden1.get_weights()
        weights2 = self.hidden2.get_weights()
        weights3 = self.hidden3.get_weights()
        
        row = [current_move.numpy().flatten(), action, no_rows, gap, loss.numpy(), 
               score, no_games, weights1, weights2, weights3, count]
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)
            
    def discount_rewards(self):
        discounted_rewards = np.array(self.rewards, dtype=np.float32)
        for step in range(len(self.rewards) - 2, -1, -1):
            discounted_rewards[step] += discounted_rewards[step + 1] * self.discount_factor
        return discounted_rewards

    def normalize_rewards(self, rewards):
        mean = np.mean(rewards)
        std = np.std(rewards)
        normalized_rewards = (rewards - mean) / (std + 1e-10)  # Add a small value to avoid division by zero
        return normalized_rewards