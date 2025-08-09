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
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import kaleido
from scipy import ndimage
from skimage import morphology, filters
import cv2

url = "IHC Cohort 2 6-4-25.lif"
lif = LifFile(url)

"""
WorkFlow
Create binary masks for each channel based on intensity thresholds
-> What is a binary mask, marks each pixel as a 0 or a 1 depending on if we care about the pixel or not
Quantify red signal area, intensity distribution
-> Red signal area is talking about the signal we care about, providing a threshold for ex like 100 we would only care about red pixels above 100, we want how big and how bright the red signal area is 
Identify colocalization regions (red AND blue above thresholds)
->Logical AND between binary masks for blue and red
Generate metrics like overlap coefficients, Manders' coefficients
-> Measures the correlation between intensities of the two channels, independent of threshold.
"""

image_list = []

for image_idx, image in enumerate(lif.get_iter_image()):
    print(f"Processing image {image_idx + 1}/48")
    print(f"Image Dimensions {image.dims}")
    z_stack_size = image.dims[2]  # 75 Z-Slices
    
    # Grab each Channel to process
    channel_max_projections = []
    
    for channel in range(3):  # 3 channels (Red, Green, Blue)
        # GRab all the Z-Slices
        z_slices = []
        for z in range(z_stack_size):
            frame = image.get_frame(z=z, t=0, c=channel)
            z_slices.append(np.array(frame))
        
        # Stack and take maximum projection for this channel
        # np.max -> for Maximum Intensity Projection
        # np.mean -> for Average Intensity Projection
        # np.sum -> for Sum Projection
        # np.median -> for median Projection
        # Could also try PCA
        z_stack = np.stack(z_slices, axis=0)  # Shape: (75, 512, 512)
        max_projection = np.median(z_stack, axis=0)  # Shape: (512, 512)
        channel_max_projections.append(max_projection)
    
    # Combine 3 channels into RGB
    rgb_image = np.stack([
        channel_max_projections[0],  # Red 
        channel_max_projections[1],  # Green 
        channel_max_projections[2]   # Blue 
    ], axis=2)                      # Shape: (512, 512, 3)
    
    # Normalize and convert to uint8
    rgb_image = (rgb_image / rgb_image.max() * 255).astype(np.uint8)
    
    # Convert to PIL and display
    composite_image = Image.fromarray(rgb_image)
    image_list.append(composite_image)