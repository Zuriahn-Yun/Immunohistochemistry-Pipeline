# Sharepoint URL 
# Reference 
# https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azureacs
import os
import requests
from readlif.reader import LifFile
import numpy as np
import time
from PIL import Image
import readlif
import extcolors

"""
------------------------------------------------------------------
lif.py is a mess, restart again with a better understanding of lif file structure
LIF File --->
        Image1 --->
            Frame1--->
                Channel1--->
                Channel2--->
                Channel3--->
            Frame2--->
        Image2--->  
------------------------------------------------------------------
"""

url = "IHC Cohort 2 6-4-25.lif"
# In this data I only have one frame per image 
lif = LifFile(url)
image_count = 0
frame_count = 0
for image in lif.get_iter_image():
    image_count +=1
    for frame in image.get_iter_t():
        frame_count +=1
        img = Image.fromarray(np.array(frame))
        colors,pixel_count = extcolors.extract_from_image(img)
        print(colors)
        
        break
    break
        
print(image_count)
print(frame_count)

basic_colors = {
    "black": [0,0,0],
    "white": [255,255,255],
    "red": [255,0,0],
    "lime": [0,255,0],
    "blue": [0,0,255],
    "yellow": [255,255,0],
    "cyan": [0,255,255],
    "magenta": [255,0,255],
    "silver": [192,192,192],
    "gray": [128,128,128],
    "maroon": [128,0,0],
    "olive": [128,128,0],
    "green": [0,128,0],
    "purple": [128,0,128],
    "teal": [0,128,128],
    "navy":[0,0,128],    
}

import math

test = [250,0,0]

distance_value = 9999999999
closest_color = "test"
for key,val in basic_colors.items():
    curr_distance = math.dist(test,val)
    if curr_distance < distance_value:
        distance_value = curr_distance
        closest_color = key
        print(distance_value)
        print(closest_color)