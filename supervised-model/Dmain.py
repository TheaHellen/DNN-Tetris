#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:29:25 2024

@author: theahellen
"""

import pygame, sys
from Dgame import Game
from Dcolors import Colors
from Dgrid import Grid

pygame.init()

title_font = pygame.font.Font(None, 40)

screen = pygame.display.set_mode((320, 620)) #setting a 300 width by 600 length pixel screen 
pygame.display.set_caption("Python Tetris") #setting a title

clock = pygame.time.Clock() #setting the frame rate of the game

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 30)

pause = False

#The game loop
while True: #initialising the game
    for event in pygame.event.get(): #looking through all the possible events
    
        if event.type == pygame.QUIT: #if the user presses the x button on the window it quits the game
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                keyInput = pygame.key.get_pressed()
                pause = not pause

        if event.type == GAME_UPDATE and game.game_over == False and pause == False:
            game.move_down()
     
    #Drawing
    screen.fill(Colors.dark_blue)
    game.draw(screen)
    
    pygame.display.update()
    clock.tick(125) #the while loop will run 60 times a second
                   #if we didn't set a frame rate the game would run as fast as possible
                   #leading to inconsistensies in speed