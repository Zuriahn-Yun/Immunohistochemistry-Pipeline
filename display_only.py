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

url = "LIF FILES\IHC Cohort 2 5-26-25.lif"
image_list = []
lif = LifFile(url)
 # Percentiles 75 = 0.75 percent
red_percentile = 75
green_percentile = 30
blue_percentile = 30

# Display each seperately and analyze that way?
# Waiting on response
total_images = sum(1 for _ in lif.get_iter_image())
for image_idx, image in enumerate(lif.get_iter_image()):
        print("URL: ",url)
        print(f"Processing image {image_idx + 1}/{total_images}")
        print(f"Image Dimensions {image.dims}")
        z_stack_size = image.dims[2]  # 75 Z-Slices
            
        # Grab each Channel to process
        channel_max_projections = []
            
        for channel in range(3):  # 3 channels (Red, Green, Blue)
            z_slices = [np.array(image.get_frame(z=z, t=0, c=channel)) 
                    for z in range(z_stack_size)]
        
            z_stack = np.stack(z_slices, axis=0)  # Shape: (Z, H, W)
                
                # Stack and take maximum projection for this channel
                # np.max -> for Maximum Intensity Projection
                # np.mean -> for Average Intensity Projection
                # np.sum -> for Sum Projection
                # np.median -> for median Projection
                # Could also try PCA
                
            # RED Channel
            if channel == 0:
                z_stack = np.stack(z_slices, axis=0)  # Shape: (75, 512, 512)
                max_projection = np.percentile(z_stack,red_percentile, axis=0)  # Shape: (512, 512)
                    
                # GREEN Channel
            elif channel == 1:
                z_stack = np.stack(z_slices, axis=0)  # Shape: (75, 512, 512)
                max_projection = np.percentile(z_stack,green_percentile, axis=0)  # Shape: (512, 512)
                    
                # BLUE Channel
            else:
                z_stack = np.stack(z_slices, axis=0)  # Shape: (75, 512, 512)
                max_projection = np.percentile(z_stack,blue_percentile, axis=0)  # Shape: (512, 512)
                    
            channel_max_projections.append(max_projection)
        # Combine 3 channels into RGB
        rgb_image = np.stack([
        channel_max_projections[0],  # Red 
            channel_max_projections[1],  # Green 
            channel_max_projections[2]   # Blue 
        ], axis=2)                      # Shape: (512, 512, 3)
            
        rgb_image_max = rgb_image.max()
         # Normalize and convert to uint8
         
        rgb_image = (rgb_image / rgb_image_max * 255).astype(np.uint8)
            
        row,column,depth = rgb_image.shape
        
        # merged = [[color, color_count[color], intensity_values[color]] for color in intensity_values]

        # # sort by intensity (3rd element, index 2)
        # sorted_merged = sorted(merged, key=lambda x: x[2], reverse=True)
            
        # lists are sorted like this [COLOR, COLOR COUNT, INTENSITY VALUES]
        # print("SORTED AND MERGED LISTS")
        # print(sorted_merged)
            
         # Convert to PIL and display
        composite_image = Image.fromarray(rgb_image)

        image_list.append(composite_image)
        
# Create output folder
output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)

for idx, img in enumerate(image_list):
    # Create subfolder (optional: group by batch of 50, etc.)
    subfolder = os.path.join(output_dir, f"batch_{idx//50 + 1}")
    os.makedirs(subfolder, exist_ok=True)

    # Save as JPEG
    save_path = os.path.join(subfolder, f"image_{idx+1}.jpeg")
    img.save(save_path, "JPEG")
    print(f"Saved {save_path}")