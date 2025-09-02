#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:30:17 2024

@author: theahellen
"""

from Dgrid import Grid
from Dblocks import *
from basic_dmodel2 import Model
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [DBlock()]
        self.current_block = DBlock()
        self.next_block = DBlock()
        self.game_over = False
        self.score = 0
        self.model = Model()
        self.game_no = 0
        
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        if lines_cleared == 2:
            self.score += 300
        if lines_cleared == 3:
            self.score += 500
        if lines_cleared == 4:
            self.score += 800
        self.score += move_down_points
    
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)
        
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)
        
    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
            
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = 1 #when blocks lock they are light grey
        self.current_block = self.next_block
        self.next_block = DBlock()
        #get grid
        input_tensor = self.grid.get_grid()
        #get move
        next_move = self.model.model_play(input_tensor, self.score, self.game_no)
        #interpret and execute move
        enumerate(next_move)
        if next_move[0] == "h":
            if next_move[1] == "1" and self.game_over == False:
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
            if next_move[1] == "2":
                self.move_left()
                self.move_left()
                self.move_left()
            if next_move[1] == "3":
                self.move_left()
                self.move_left()
            if next_move[1] == "4":
                self.move_left()
            if next_move[1] == "6":
                self.move_right()
            if next_move[1] == "7":
                self.move_right()
                self.move_right()
            if next_move[1] == "8":
                self.move_right()
                self.move_right()
                self.move_right()
            if next_move[1] == "9":
                self.move_right()
                self.move_right()
                self.move_right()
                self.move_right()
        if next_move[0] == "v" and self.game_over == False:
            self.rotate()
            if next_move[1] == "1":
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
            if next_move[1] == "2":
                self.move_left()
                self.move_left()
                self.move_left()
                self.move_left()
            if next_move[1] == "3":
                self.move_left()
                self.move_left()
                self.move_left()
            if next_move[1] == "4":
                self.move_left()
                self.move_left()
            if next_move[1] == "5":
                self.move_left()
            if next_move[1] == "7":
                self.move_right()
            if next_move[1] == "8":
                self.move_right()
                self.move_right()
            if next_move[1] == "9":
                self.move_right()
                self.move_right()
                self.move_right()
            if next_move[1] == "0":
                self.move_right()
                self.move_right()
                self.move_right()
                self.move_right()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        #self.grid.print_grid() #prints the grid to the console
        #if self.block_fits() == False:
        if self.grid.is_row_empty(0) == False:
            self.game_over = True
            
    def reset(self):
        self.grid.reset()
        self.blocks = [DBlock()]
        self.current_block = DBlock()
        self.next_block = DBlock()
        self.score = 0
        self.game_no += 1
        self.game_over = False
            
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False and self.grid.is_row_full(19) == False:
                return False
        self.model.model.save('model.keras')
        return True
            
    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False: 
            self.current_block.undo_rotation()
     
    def anti_rotate(self):
        self.current_block.undo_rotation()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.rotate()
            
    def rotate_180(self):
        self.current_block.rotate()
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.rotate()
            self.current_block.rotate()
        
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True
    
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        self.next_block.draw(screen, 255, 280)
        
        
        
    
        