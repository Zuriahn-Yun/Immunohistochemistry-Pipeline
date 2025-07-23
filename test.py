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
        
print(image_count)
print(frame_count)


