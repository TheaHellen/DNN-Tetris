#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:31:01 2024

@author: theahellen
"""

import pygame
import numpy as np
import os
import tensorflow as tf
from PIL import Image
from Dcolors import Colors

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        #creating a 10x20 grid (list of lists) of 0s:
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()
        # Pick a random scenario
        self.scenario_no = np.random.randint(1, 20)
        self.grid_pass = self.scenario(self.scenario_no)
        self.grid[18:19] = self.grid_pass

    # Create the scenarios
    def scenario(self, num): # num can take values 1 to 19
        # Create the grid
        grid = np.zeros((2, 10))

        if num <= 10:
            for i in range(10):
                grid[1, i] = 1
                grid[0, i] = 1
            grid[1, num-1] = 0
            grid[0, num-1] = 0
        else:
            for i in range(10):
                grid[1, i] = 1
            grid[1, num-11] = 0
            grid[1, num-10] = 0
        return grid
        
    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()
            
    def get_grid(self):
        #return the grid in the correct format for the model
        grid = self.grid_pass
        tensor = tf.constant(grid, dtype=tf.float32)
        input_tensor = tf.expand_dims(tensor, axis=0)
        return input_tensor
            
    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column>=0 and column < self.num_cols:
            return True
        else:
            return False
        
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False
    
    def is_row_empty(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] != 0:
                return False
        return True
    
    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True
    
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0
            
    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0
            
    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0
        # Pick a random scenario
        self.scenario_no = np.random.randint(1, 20)
        self.grid_pass = self.scenario(self.scenario_no)
        self.grid[18:19] = self.grid_pass
            
    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size +11, row*self.cell_size +11, 
                                        self.cell_size -1, self.cell_size -1)
                pygame.draw.rect(screen, self.colors[int(cell_value)], cell_rect)
                