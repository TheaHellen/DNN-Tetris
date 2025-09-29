#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:31:55 2024

@author: theahellen
"""

class Colors:
    dark_grey = (26, 31, 40)
    orange = (226, 116, 17)
    blue = (13, 64, 216)
    cyan = (21, 204, 209)
    yellow = (237, 234, 4)
    green = (47, 230, 23)
    purple = (166, 0, 247)
    red = (232, 18, 18)
    light_grey = (160, 160, 160)
    white = (255, 255, 255)
    dark_blue = (44, 44, 127)
    light_blue = (59, 85, 162)

    
    @classmethod 
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.light_grey]