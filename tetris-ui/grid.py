#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 16:27:37 2024

@author: theahellen
"""

#Import packages
import pygame
#Import colors class
from colors import Colors

#Define the grid class
class Grid:
    def __init__(self):
        #Set the dimensions of the grid
        self.num_rows = 20
        self.num_cols = 10
        #Set the cell size
        self.cell_size = 30
        #Create the grid as a list of lists
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()
       
    #Method to print the grid to the console
    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()
    
    #Method to check if a cell is inside the dimensions of the grid
    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column>=0 and column < self.num_cols:
            return True
        else:
            return False
    
    #Method to check if the grid is empty at a certain cell
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False
    
    #Method to check if a row is full
    def is_row_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True
    
    #Method to clear a row
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0
    
    #Method to move a row down by any number of rows
    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0
    
    #Method to clear and move down rows after the user fills any number of rows
    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    
    #Method to reset the grid to 0s
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0
     
    #Method to draw the grid (not the blocks)
    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size +11, row*self.cell_size +11, 
                                        self.cell_size -1, self.cell_size -1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)
                