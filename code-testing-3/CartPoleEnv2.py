#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 15:24:24 2025

@author: theahellen
"""

import gym
import numpy as np
import tensorflow as tf
from tensorflow import keras

env = gym.make("CartPole-v1", render_mode="human")
obs = env.reset()

# MOVE THE CART RIGHT BY ONE
'''
print(obs)
#print(env.action_space)

#accelerate right
action = 1 
obs, reward, terminated, truncated, info = env.step(action)
done = terminated or truncated
print(obs)
print(reward)
print(done)
print(info)
'''
# MOVE THE CART RIGHT OR LEFT DEPENDING ON THE ANGLE - 500 TIMES TO SEE HOW 
# WELL IT DOES
'''
def basic_policy(obs): 
    angle = obs[2]
    return 0 if angle < 0 else 1
    
totals = []

for episode in range(500):
    episode_rewards = 0
    obs, info = env.reset()
    for step in range(200):
            action = basic_policy(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            episode_rewards += reward
            if done:
                break
    totals.append(episode_rewards)
    
print(np.mean(totals))
print(np.std(totals))
print(np.min(totals))
print(np.max(totals))
'''
# NEURAL NETWORK

#build the neural network
n_inputs = 4 # == env.observation_space.shape[0]
model = keras.models.Sequential([
    keras.Input(shape=(n_inputs,)),
    keras.layers.Flatten(),
    keras.layers.Dense(5, activation="elu"),
    keras.layers.Dense(1, activation="sigmoid"),
])

#train the neural network using a REINFORCE PG algorithm

def play_one_step(env, obs, model, loss_fn): 
    with tf.GradientTape() as tape: #this allows calculations of the gradients
        #get the probability of going left
        left_proba = model(obs[np.newaxis]) #call the model by giving it a single 
                                            #observation - reshaped in batch form
        #determine the target probability of going left
        action = (tf.random.uniform([1, 1]) > left_proba)
        #define the target probability of going left
        y_target = tf.constant([[1.]]) - tf.cast(action, tf.float32)
        #compute the loss using the given loss function
        loss = tf.reduce_mean(loss_fn(y_target, left_proba))
    #compute the gradients
    grads = tape.gradient(loss, model.trainable_variables)
    #play the selected action
    obs, reward, terminated, truncated, info = env.step(int(action[0, 0].numpy()))
    done = terminated or truncated
    return obs, reward, done, grads

def play_multiple_episodes(env, n_episodes, n_max_steps, model, loss_fn): 
    all_rewards = []
    all_grads = []
    for episode in range(n_episodes):
        current_rewards = [] 
        current_grads = []
        obs, info = env.reset()
        for step in range(n_max_steps):
            obs, reward, done, grads = play_one_step(env, obs, model, loss_fn) 
            current_rewards.append(reward)
            current_grads.append(grads)
            if done:
                break
        all_rewards.append(current_rewards)
        all_grads.append(current_grads) 
    #returns a list of reward lists - one reward list per episode with one reward per step
    #returns a list of gradient lists - one gradients list per episode, with one
        #tuple of gradients per step, tuple contains one gradient tensor per trainable
        #variable
    return all_rewards, all_grads

#compute the sum of future discounted rewards at each step
def discount_rewards(rewards, discount_factor): 
    discounted = np.array(rewards)
    for step in range(len(rewards) - 2, -1, -1):
        discounted[step] += discounted[step + 1] * discount_factor 
    return discounted

#normalize all the discounted rewards (returns) across many episodes
def discount_and_normalize_rewards(all_rewards, discount_factor): 
    all_discounted_rewards = [discount_rewards(rewards, discount_factor)
                              for rewards in all_rewards]
    flat_rewards = np.concatenate(all_discounted_rewards)
    reward_mean = flat_rewards.mean()
    reward_std = flat_rewards.std()
    return [(discounted_rewards - reward_mean) / reward_std
            for discounted_rewards in all_discounted_rewards]

n_iterations = 150
n_episodes_per_update = 10
n_max_steps = 200
discount_factor = 0.95

optimizer = keras.optimizers.Adam(learning_rate=0.01)
loss_fn = keras.losses.binary_crossentropy

for iteration in range(n_iterations):
    all_rewards, all_grads = play_multiple_episodes(
            env, n_episodes_per_update, n_max_steps, model, loss_fn)
    all_final_rewards = discount_and_normalize_rewards(all_rewards,
                                                              discount_factor)
    all_mean_grads = []
    for var_index in range(len(model.trainable_variables)):
        mean_grads = tf.reduce_mean(
            [final_reward * all_grads[episode_index][step][var_index]
             for episode_index, final_rewards in enumerate(all_final_rewards) 
                 for step, final_reward in enumerate(final_rewards)], axis=0)
        all_mean_grads.append(mean_grads)
    optimizer.apply_gradients(zip(all_mean_grads, model.trainable_variables))






