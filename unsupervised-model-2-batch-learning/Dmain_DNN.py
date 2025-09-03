#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 18:50:39 2025

@author: theahellen
"""

import pygame, sys
from Dgame import Game
from Dcolors import Colors
from Dgrid import Grid

pygame.init()

game = Game()
grid = Grid()

pause = False

#The game loop
while True: #initialising the game
    for event in pygame.event.get(): #looking through all the possible events
    
        if event.type == pygame.QUIT: #if the user presses the x button on the window it quits the game
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN: #if the user presses the spacebar the game loop pauses
            if event.key == pygame.K_SPACE:
                keyInput = pygame.key.get_pressed()
                pause = not pause
            
    if game.game_over == True:
        game.reset()
            
    if game.game_over == False and pause == False:
        game.move_down()
