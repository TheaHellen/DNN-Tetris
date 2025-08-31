#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:39:17 2024

@author: theahellen
"""

#Import packages
import pygame, sys
#Import game and colors classes
from game import Game
from colors import Colors

#Initialise pygame
pygame.init()

#Create surfaces
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
hold_surface = title_font.render("Hold", True, Colors.white)

#Create rectangles to surround the score, next block and hold
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215-40, 170, 180)
hold_rect = pygame.Rect(320, 215, 170, 180)

#Set the dimensions of the screen
screen = pygame.display.set_mode((500, 620))

#Set the window title
pygame.display.set_caption("Python Tetris")

#Initialise time
clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
#Set the block to move down every 200 milliseconds
pygame.time.set_timer(GAME_UPDATE, 200)

print(type(game.current_block))

#The Game Loop
while True: 
    #Iterate through all possible events
    for event in pygame.event.get(): 
        
        #If the user presses the x button on the window it quits the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        #If the user presses a key
        if event.type == pygame.KEYDOWN:
            keyInput = pygame.key.get_pressed()
            #If the user presses a key the game carries on
            if game.game_over == True: 
                game.reset()
            #If the user presses a the block moves to the left
            if keyInput[pygame.K_a] and game.game_over == False:
                game.move_left()
            #If the user presses d the block moves to the right
            if keyInput[pygame.K_d] and game.game_over == False:
                game.move_right()
            #If the user presses s the block moves down
            if keyInput[pygame.K_s] and game.game_over == False:
                game.move_down()
                #The score is updated by 1 every time the user moves the block down
                game.update_score(0, 1)
            #If the user presses the space bar the block rotates clockwise
            if keyInput[pygame.K_SPACE] and game.game_over == False:
                game.rotate()
            #If the user presses e the block rotates anticlockwise
            if keyInput[pygame.K_e] and game.game_over == False:
                game.anti_rotate()
            #If the user presses q the block rotates 180 degrees
            if keyInput[pygame.K_q] and game.game_over == False:
                game.rotate_180()
            #If the user presses shift they access the hold
            if keyInput[pygame.K_LSHIFT] and game.game_over == False:
                game.hold_block()
            #If the user presses w the block hard drops
            if keyInput[pygame.K_w] and game.game_over == False:
                game.hard_drop()
        #The block moves down every 200 milliseconds
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
     
    #Draw the screen
    #Display the score
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    
    #Set the background to be dark blue
    screen.fill(Colors.dark_blue)
    
    #Draw the score, next block and hold surfaces
    screen.blit(score_surface, (365, 20, 50, 50)) 
    screen.blit(next_surface, (375, 180-40, 50, 50)) 
    screen.blit(hold_surface, (375, 380, 50, 50))
        
    #If the game is over, display game over text
    if game.game_over == True:
        screen.blit(game_over_surface, (320, 450, 50,  50))
    
    #Draw the rectangle around the score
    pygame.draw.rect(screen, Colors.dark_grey, score_rect, 0, 10)
    #Centre the score inside the rectangle
    screen.blit(score_value_surface, score_value_surface.get_rect(
        centerx = score_rect.centerx, centery = score_rect.centery))
    #Draw the rectangle around the next block
    pygame.draw.rect(screen, Colors.dark_grey, next_rect, 0, 10)

    game.draw(screen)

    
    pygame.display.update()
    #Set the frame rate to 60 frames per second (the while loop will run 60 
    #times a second)
    clock.tick(60)
                   
    