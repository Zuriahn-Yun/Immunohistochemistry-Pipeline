import os
import requests
from readlif.reader import LifFile
import numpy as np
import time
from PIL import Image
import readlif
import extcolors
import math
import pandas as pd 

"""
------------------------------------------------------------------
lif.py is a mess, restart again with a better understanding of lif file structure
LIF File --->
        Image1 --->
            Frame1--->
                Channel1--->
                    Z-slices[1] --->
                    Z-slices[2] --->
                    ...
                    Z-slices[75] -->
                Channel2--->
                Channel3--->
            Frame2--->
        Image2--->  
Do a max projection over Z per channel -> 3 Flattened images
Stack them -> RGB Images.....
------------------------------------------------------------------
"""

def darkness_luminosity(row):
  """ Using the NTSC formula to convert RGB values into Grayscale, this formula closely represents the average persons relative perception of brighness in red,green and blue light. Smaller values represent darker pixels.

  Args:
      row (int): a row from an image dataframe and contains red,green and blue columns
  Returns:
      int : darkness value
  """
  #print(row)
  return (0.299 * row[0] + 0.587 * row[1] + 0.114 * row[2])

def closest_color(rgb):
    basic_colors = {
    "Black": [0,0,0],
    "White":[255,255,255],
    "BLue":[0,0,28],
    "Green": [0,20,0],
    "Red":[28,0,0],
    }
    
    distance_value = 9999999999
    closest_color = "test"
    
    for key,val in basic_colors.items():
        curr_distance = math.dist(rgb,val)
        if curr_distance < distance_value:
            distance_value = curr_distance
            closest_color = key
    return closest_color

# url = "IHC Cohort 2 6-4-25.lif"


# In this data I only have one frame per image 
# lif = LifFile(url)
# image_count = 0
# frame_count = 0
# colors = []
# for image in lif.get_iter_image():
#     image_count +=1
#     print(image.dims)
#     curr = image.get_frame()
#     for frame in image.get_iter_t():
#         frame_count +=1
#         for i in range(3):
#             frame = image.get_frame(c=i)
#         frame = image.get_frame(c=2)
#         img_array = np.array(frame)
#         print("IMAGE ARRAY")
#         print(img_array)
#         print(img_array.shape)
#         for row in img_array:
#             color = closest_color(rgb=row)
#             colors.append(color) 
#     print(colors)
#     exit()