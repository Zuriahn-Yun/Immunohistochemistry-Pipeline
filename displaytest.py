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

url = "IHC Cohort 2 6-4-25.lif"

lif = LifFile(url)
image_count = 0
frame_count = 0
colors = []
for image in lif.get_iter_image():
    
    image_count +=1
    print("Image Dimensions: ",image.dims)
    
    x_size = image.dims[0]
    y_size = image.dims[1]
    z_stack = image.dims[2]
    t_val = image.dims[3]
    m_val = image.dims[4]
    
    curr = image.get_frame()
    
    for frame in image.get_iter_t():
        frame_count+=1
        print("Frame Size: ",frame.size)
        
        for z in range(z_stack):
            frame = image.get_frame(z=z, t=0)
            
            # Size (512,512)
            
            
print("Image Count:", image_count)
print("Frame Count:", frame_count)