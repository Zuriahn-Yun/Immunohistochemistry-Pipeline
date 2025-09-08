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
from analyzefinal import closest_color,darkness_luminosity,process_image
import plotly.express as px

url = "IHC Cohort 2 6-4-25.lif"
lif = LifFile(url)

image_list = []


# These dont get used, here as a reference
basic_colors = {
    "Black": [0,0,0],
    "White": [255,255,255],
    "Red": [255,0,0],
    "Lime": [0,255,0],
    "Blue": [0,0,255],
    "Yellow": [255,255,0],
    "Cyan": [0,255,255],
    "Magenta": [255,0,255],
    "Silver": [192,192,192],
    "Gray": [128,128,128],
    "Maroon": [128,0,0],
    "Olive": [128,128,0],
    "Green": [0,128,0],
    "Purple": [128,0,128],
    "Teal": [0,128,128],
    "Navy":[0,0,128],    
    }

# Percentiles 75 = 0.75 percent
red_percentile = 75
green_percentile = 30
blue_percentile = 30

# Display each seperately and analyze that way?
# Waiting on response

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
        
        # RED Channel
        if channel == 0:
            z_stack = np.stack(z_slices, axis=0)  # Shape: (75, 512, 512)
            max_projection = np.percentile(z_stack,red_percentile, axis=0)  # Shape: (512, 512)
            
        # GREEN Channel
        if channel == 1:
            z_stack = np.stack(z_slices, axis=0)  # Shape: (75, 512, 512)
            max_projection = np.percentile(z_stack,green_percentile, axis=0)  # Shape: (512, 512)
            
        # BLUE Channel
        if channel == 2:
            z_stack = np.stack(z_slices, axis=0)  # Shape: (75, 512, 512)
            max_projection = np.percentile(z_stack,blue_percentile, axis=0)  # Shape: (512, 512)
            
        channel_max_projections.append(max_projection)
    # Combine 3 channels into RGB
    rgb_image = np.stack([
        channel_max_projections[0],  # Red 
        channel_max_projections[1],  # Green 
        channel_max_projections[2]   # Blue 
    ], axis=2)                      # Shape: (512, 512, 3)
    
    # Normalize and convert to uint8
    rgb_image = (rgb_image / rgb_image.max() * 255).astype(np.uint8)
    
    row,column,depth = rgb_image.shape
    
    color_count = {
    "Black": 0,
    "White": 0,
    #"#001400(Very Dark Green)":0,
    "Green": 0,
    #"1c0000(Very Dark Red)":0,
    "Red": 0,
    #"#00001c(Very Dark Blue)":0,
    "Blue": 0,
    }
    
    # Dictionary to hold the Intensity summations -> each pixel has an intensity, we will just sum it all together for whichever category it is and from there decide
    # Which is the most intense
    intensity_values = {
        "Black" : 0,
        "White": 0,
        "Green": 0,
        "Red": 0,
        "Blue": 0,
    }
    
    for r in range(row):
        for c in range(column):
            red_val,green_Val,blue_val = rgb_image[r,c]
            pixel = [red_val,green_Val,blue_val]
            color  = closest_color(pixel)
            
            # Get the intensity here 
            intensity = darkness_luminosity(rgb_image[r,c])
            
            if color in color_count:
                color_count[color] +=1
                intensity = darkness_luminosity(rgb_image[r,c])
                intensity_values[color] += int(intensity)
            else:
                print("Error Color Not Found")
                
    
    
    print("INTENSITY")
    print(intensity_values)  
    print("COLOR COUNT") 
    print(color_count)
    merged = [[color, color_count[color], intensity_values[color]] for color in intensity_values]

    # sort by intensity (3rd element, index 2)
    sorted_merged = sorted(merged, key=lambda x: x[2], reverse=True)
    
    # lists are sorted like this [COLOR, COLOR COUNT, INTENSITY VALUES]
    print("SORTED AND MERGED LISTS")
    print(sorted_merged)
       
    exit()
    
    # Convert to PIL and display
    composite_image = Image.fromarray(rgb_image)

    image_list.append(composite_image)
    
    fig = px.imshow(composite_image)
    fig.show()
    
    
np_images = [np.array(img) for img in image_list]
total = len(np_images)
cols = 6 
rows = (total + cols - 1) // cols

fig = make_subplots(rows=rows, cols=cols, subplot_titles=[f"Image {i+1}" for i in range(total)])

for idx, img in enumerate(image_list):
    row = idx // cols + 1
    col = idx % cols + 1

     # Add image to subplot
    fig.add_trace(
        go.Image(z=img),
        row=row, col=col
    )


# Certain pixels are green but are not being registered as close to green when analysis is done 
# Try changing the gamma 
fig.update_layout(height=512*rows, width=512*cols, title_text="IHC Cohort 2 6-4-25: Red Percentile: " + str(red_percentile) + ", Blue Percentile: " + str(blue_percentile) + ", Green Percentile: " + str(green_percentile))
fig.show()
