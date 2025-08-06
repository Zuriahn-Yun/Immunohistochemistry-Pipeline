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

def adjust_intensity(channel_data, percentile_clip=99.5, gamma=1.0):
    """
    Adjust intensity to reduce overexposure
    
    Parameters:
    - channel_data: 2D numpy array of channel intensities
    - percentile_clip: Clip values above this percentile (reduces overexposure)
    - gamma: Gamma correction value (< 1 brightens, > 1 darkens)
    """
    # Clip extreme values
    upper_limit = np.percentile(channel_data, percentile_clip)
    channel_clipped = np.clip(channel_data, 0, upper_limit)
    
    # Normalize to 0-1
    normalized = channel_clipped / upper_limit
    
    # Apply gamma correction
    gamma_corrected = np.power(normalized, gamma)
    
    # Scale to 0-255
    return (gamma_corrected * 255).astype(np.uint8)

def create_channel_mask(channel_data, threshold_method='otsu', min_area=100):
    """
    Create binary mask for a channel
    
    Parameters:
    - channel_data: 2D numpy array
    - threshold_method: 'otsu', 'adaptive', or 'manual'
    - min_area: Minimum area for connected components to keep
    """
    if threshold_method == 'otsu':
        threshold = filters.threshold_otsu(channel_data)
    elif threshold_method == 'adaptive':
        threshold = filters.threshold_local(channel_data, block_size=35)
        return channel_data > threshold
    else:  # manual threshold
        threshold = np.percentile(channel_data, 75)  # Adjust as needed
    
    # Create binary mask
    mask = channel_data > threshold
    
    # Remove small objects (noise)
    mask = morphology.remove_small_objects(mask, min_size=min_area)
    
    # Fill small holes
    mask = morphology.remove_small_holes(mask, area_threshold=min_area//2)
    
    return mask

def remove_capillaries(red_mask, blue_mask, min_width=3, max_width=15):
    """
    Remove capillary-like structures (thin, elongated objects)
    
    Parameters:
    - mask: Binary mask
    - min_width: Minimum width to consider as capillary
    - max_width: Maximum width to consider as capillary
    """
    # Use morphological operations to identify thin structures
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (max_width, max_width))
    
    # Opening operation to remove thin structures
    red_cleaned = cv2.morphologyEx(red_mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
    blue_cleaned = cv2.morphologyEx(blue_mask.astype(np.uint8), cv2.MORPH_OPEN, kernel)
    
    return red_cleaned.astype(bool), blue_cleaned.astype(bool)

def analyze_colocalization(red_mask, blue_mask, red_intensity, blue_intensity):
    """
    Analyze colocalization between red and blue channels
    """
    # Colocalization mask
    coloc_mask = red_mask & blue_mask
    
    # Calculate metrics
    red_area = np.sum(red_mask)
    blue_area = np.sum(blue_mask)
    coloc_area = np.sum(coloc_mask)
    
    # Colocalization coefficients
    manders_m1 = np.sum(red_intensity[coloc_mask]) / np.sum(red_intensity[red_mask]) if red_area > 0 else 0
    manders_m2 = np.sum(blue_intensity[coloc_mask]) / np.sum(blue_intensity[blue_mask]) if blue_area > 0 else 0
    
    # Overlap coefficient
    overlap_coeff = coloc_area / (red_area + blue_area - coloc_area) if (red_area + blue_area - coloc_area) > 0 else 0
    
    return {
        'red_area': red_area,
        'blue_area': blue_area,
        'coloc_area': coloc_area,
        'manders_m1': manders_m1,  # Red overlapping with blue
        'manders_m2': manders_m2,  # Blue overlapping with red
        'overlap_coefficient': overlap_coeff,
        'red_mean_intensity': np.mean(red_intensity[red_mask]) if red_area > 0 else 0,
        'blue_mean_intensity': np.mean(blue_intensity[blue_mask]) if blue_area > 0 else 0,
        'coloc_mean_red_intensity': np.mean(red_intensity[coloc_mask]) if coloc_area > 0 else 0,
        'coloc_mean_blue_intensity': np.mean(blue_intensity[coloc_mask]) if coloc_area > 0 else 0
    }

# Process images with intensity adjustment
image_list = []
analysis_results = []

# Intensity adjustment parameters - modify these to optimize your images
RED_PERCENTILE_CLIP = 98.0  # Clip red values above this percentile
BLUE_PERCENTILE_CLIP = 99.0  # Clip blue values above this percentile
RED_GAMMA = 1.2  # Gamma correction for red (> 1 darkens)
BLUE_GAMMA = 1.0  # Gamma correction for blue

for image_idx, image in enumerate(lif.get_iter_image()):
    print(f"Processing image {image_idx + 1}/48")
    print(f"Image Dimensions {image.dims}")
    z_stack_size = image.dims[2]  # 75 Z-Slices
    
    # Grab each Channel to process
    channel_projections = []
    
    for channel in range(3):  # 3 channels (Red, Green, Blue)
        # Grab all the Z-Slices
        z_slices = []
        for z in range(z_stack_size):
            frame = image.get_frame(z=z, t=0, c=channel)
            z_slices.append(np.array(frame))
        
        # Stack and take median projection for this channel
        z_stack = np.stack(z_slices, axis=0)  # Shape: (75, 512, 512)
        projection = np.median(z_stack, axis=0)  # Shape: (512, 512)
        channel_projections.append(projection)
    
    # Apply intensity adjustments
    red_adjusted = adjust_intensity(channel_projections[0], 
                                  percentile_clip=RED_PERCENTILE_CLIP, 
                                  gamma=RED_GAMMA)
    green_adjusted = adjust_intensity(channel_projections[1], 
                                    percentile_clip=99.0, 
                                    gamma=1.0)  # Green same as red per your note
    blue_adjusted = adjust_intensity(channel_projections[2], 
                                   percentile_clip=BLUE_PERCENTILE_CLIP, 
                                   gamma=BLUE_GAMMA)
    
    # Create masks for analysis
    red_mask = create_channel_mask(channel_projections[0], threshold_method='otsu')
    blue_mask = create_channel_mask(channel_projections[2], threshold_method='otsu')
    
    # Remove capillary-like structures
    red_mask_clean, blue_mask_clean = remove_capillaries(red_mask, blue_mask)
    
    # Analyze colocalization
    coloc_results = analyze_colocalization(red_mask_clean, blue_mask_clean, 
                                         channel_projections[0], channel_projections[2])
    coloc_results['image_idx'] = image_idx + 1
    analysis_results.append(coloc_results)
    
    # Create composite image with adjusted intensities
    rgb_image = np.stack([red_adjusted, green_adjusted, blue_adjusted], axis=2)
    composite_image = Image.fromarray(rgb_image)
    image_list.append(composite_image)
    
    # Print some stats for this image
    print(f"  Red area: {coloc_results['red_area']}")
    print(f"  Blue area: {coloc_results['blue_area']}")
    print(f"  Colocalization area: {coloc_results['coloc_area']}")
    print(f"  Manders M1 (red overlapping blue): {coloc_results['manders_m1']:.3f}")
    print(f"  Overlap coefficient: {coloc_results['overlap_coefficient']:.3f}")

# Create visualization
total = len(image_list)
cols = 6 
rows = (total + cols - 1) // cols

fig = make_subplots(rows=rows, cols=cols, 
                    subplot_titles=[f"Image {i+1}" for i in range(total)])

for idx, img in enumerate(image_list):
    row = idx // cols + 1
    col = idx % cols + 1
    fig.add_trace(go.Image(z=img), row=row, col=col)

fig.update_layout(height=512*rows, width=512*cols, 
                  title_text="IHC Cohort 2 6-4-25: Intensity Adjusted with Median Projection")
fig.show()

# Create analysis results dataframe
results_df = pd.DataFrame(analysis_results)
print("\nAnalysis Summary:")
print(results_df.describe())

# Save results
results_df.to_csv('ihc_analysis_results.csv', index=False)

# Create additional visualizations for analysis
fig_analysis = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Red Area vs Image', 'Colocalization Area vs Image', 
                   'Manders M1 Coefficient', 'Overlap Coefficient'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

# Red area plot
fig_analysis.add_trace(
    go.Scatter(x=results_df['image_idx'], y=results_df['red_area'], 
              mode='lines+markers', name='Red Area'),
    row=1, col=1
)

# Colocalization area plot
fig_analysis.add_trace(
    go.Scatter(x=results_df['image_idx'], y=results_df['coloc_area'], 
              mode='lines+markers', name='Coloc Area', line=dict(color='purple')),
    row=1, col=2
)

# Manders M1 coefficient
fig_analysis.add_trace(
    go.Scatter(x=results_df['image_idx'], y=results_df['manders_m1'], 
              mode='lines+markers', name='Manders M1', line=dict(color='red')),
    row=2, col=1
)

# Overlap coefficient
fig_analysis.add_trace(
    go.Scatter(x=results_df['image_idx'], y=results_df['overlap_coefficient'], 
              mode='lines+markers', name='Overlap Coeff', line=dict(color='orange')),
    row=2, col=2
)

fig_analysis.update_layout(height=800, width=1200, title_text="IHC Analysis Metrics")
fig_analysis.show()

print(f"\nProcessing complete! Analyzed {len(image_list)} images.")
print("Results saved to 'ihc_analysis_results.csv'")


# not a clue what is happening in this file, experimenting with what rosa wants????