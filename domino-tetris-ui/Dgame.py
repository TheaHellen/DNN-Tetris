#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:30:17 2024

@author: theahellen
"""

from Dgrid import Grid
from Dblocks import *
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [DBlock()]
        self.current_block = DBlock()
        self.next_block = DBlock()
        self.game_over = False
        self.score = 0
        
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
        print("i")
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        self.grid.print_grid() #prints the grid to the console
        #if self.block_fits() == False:
        if self.grid.is_row_empty(0) == False:
            self.game_over = True
            
    def reset(self):
        self.grid.reset()
        self.blocks = [DBlock()]
        self.current_block = DBlock()
        self.next_block = DBlock()
        self.score = 0
        self.game_over = False
            
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
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
        
        
    
        