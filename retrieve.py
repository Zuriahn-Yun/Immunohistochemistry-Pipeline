# Sharepoint URL 
# Reference 
# https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azureacs
import os
import requests
from readlif.reader import LifFile
import numpy as np
import time

"""
TEST SCRIPT FOR POWER AUTOMATE
RUNNING ON A SMALL LIF FILE 
"""
path = "IHC Cohort 2 6-4-25.lif"

lif_file = LifFile(path)

data = []
frame_count = 1
for image in lif_file.get_iter_image():
    curr = []
    for frame in image.get_iter_t():
        arr = np.array(frame)
        print(arr)
        arr.flatten()
        print(arr)
        
        curr.append(arr)
        print(frame_count)
        frame_count+=1
        print(arr.shape)
    print(len(curr))
    print("Finished an Image")
    data.append(curr)

import pandas as pd

df = pd.DataFrame(data)

df.to_csv('data.csv',index=False)