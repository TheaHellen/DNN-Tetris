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
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620)) #setting a 300 width by 600 length pixel screen 
pygame.display.set_caption("Python Tetris") #setting a title

clock = pygame.time.Clock() #setting the frame rate of the game

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

#The game loop
while True: #initialising the game
    for event in pygame.event.get(): #looking through all the possible events
    
        if event.type == pygame.QUIT: #if the user presses the x button on the window it quits the game
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN: #using wasd controls
            keyInput = pygame.key.get_pressed()
            if game.game_over == True:
                game.reset()
            if keyInput[pygame.K_a] and game.game_over == False:
                game.move_left()
            if keyInput[pygame.K_d] and game.game_over == False:
                game.move_right()
            if keyInput[pygame.K_s] and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if keyInput[pygame.K_SPACE] and game.game_over == False:
                game.rotate()
            if keyInput[pygame.K_e] and game.game_over == False:
                game.anti_rotate()
            if keyInput[pygame.K_q] and game.game_over == False:
                game.rotate_180()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
     
    #Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    
    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))
    
    if game.game_over == True:
        screen.blit(game_over_surface, (320, 450, 50,  50))
        
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx,
                                                                  centery = score_rect.centery))
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    game.draw(screen)

    #Grid.print_grid(Grid())
    
    pygame.display.update()
    clock.tick(125) #the while loop will run 60 times a second
                   #if we didn't set a frame rate the game would run as fast as possible
                   #leading to inconsistensies in speed