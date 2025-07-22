from analyze import get_rgb
from readlif.reader import LifFile
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import time
from plotly.subplots import make_subplots
import pandas as pd 
from functools import reduce
import os
import extcolors
import kaleido

def delete_lif(file_path):
    """ This will delete a lif file, they are typically very large and deleting them can save space to analyze another.

    Args:
        file_path (string): The local file path.
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print("File at: " + str(file_path) + " removed successfully.")
        except Exception as e:
            print("Error " + str(e))
    else:
        print("File not found.")
            
def display_lif(file_path,rows,columns):
    """ This displays a lif file in plotly

    Args:
        file_path (string): Local file path.
        rows (int): The number of rows in the image.
        columns (int): The number of columns in the image.

    Returns:
        np.array : Displays and returns the full lif file in np.array form
    """
    
    # add all the images to one list
    images = []
    lif = LifFile(file_path)
    for image in lif.get_iter_image():
        print(image)
        for frame in image.get_iter_t():
            np_image = np.array(frame)
            images.append(np_image)
    
    # Concat every row and add to a list
    row_dataframes = []

    for i in range(rows):
        curr = []
        for k in range(columns):
            df = pd.DataFrame(images[(i * columns) + k])
            curr.append(df)
        curr_row = pd.concat(curr,axis=1,ignore_index=True)
        row_dataframes.append(curr_row)
    
    # Concat all the rows into one very large dataframe
    result = pd.concat(row_dataframes, axis=0,ignore_index=True)

    # Display the final image
    fig = px.imshow(result)
    fig.show()   
    
    # Return the Dataframe
    return result

def lif_to_df(file_path,rows,columns):
    """ This displays a lif file in plotly

    Args:
        file_path (string): Local file path.
        rows (int): The number of rows in the image.
        columns (int): The number of columns in the image.

    Returns:
        np.array : Returns the full lif file in np.array form
    """
    
    # add all the images to one list
    images = []
    lif = LifFile(file_path)
    for image in lif.get_iter_image():
        #print(image)
        for frame in image.get_iter_t():
            np_image = np.array(frame)
            images.append(np_image)
    
    # Concat every row and add to a list
    row_dataframes = []

    for i in range(rows):
        curr = []
        for k in range(columns):
            df = pd.DataFrame(images[(i * columns) + k])
            curr.append(df)
        curr_row = pd.concat(curr,axis=1,ignore_index=True)
        row_dataframes.append(curr_row)
    
    # Concat all the rows into one very large dataframe
    lif_array = pd.concat(row_dataframes, axis=0,ignore_index=True)

    # Return the Dataframe
    return lif_array
    
def export_images(lif_dataframe, name):
    # Use kaleido to save as a png and put in the export folder
    fig = px.imshow(lif_dataframe)
    fig.write_image("export_images/" + str(name) + ".png")
    
def display_individual_frames(file_path,rows,columns):
    lif = LifFile(file_path)
    fig = make_subplots(rows=rows,cols=columns)
    curr_column = 1
    curr_row = 1
    images = []
    for image in lif.get_iter_image():
         for frame in image.get_iter_t():
            np_image = np.array(frame)
            trace = px.imshow(np_image).data[0]
            images.append(trace)
            
    image_index = 0
    for i in range(1,rows+1,1):
        for j in range(1,columns+1,1):
            fig.add_trace(images[image_index],row = i,col=j)
            image_index+=1
    fig.show()

def analyze_lif(lif_dataframe):
    
    # this might be the goat color package
    # https://pypi.org/project/extcolors/
    
    colors, pixel_count = extcolors.extract_from_path("gameboy.png")
    print("error")

    
def analyze_lifext(lif_ext_path):
    # This does not work 
    # https://pypi.org/project/liffile/
    print(lif_ext_path)
    
def get_count_images(file_path):
    images = []
    lif = LifFile(file_path)
    for image in lif.get_iter_image():
        for frame in image.get_iter_t():
            np_image = np.array(frame)
            images.append(np_image)
    print("Image Count: " + str(len(images)))
    
    # To display the image in plotly you will need to provide dimensions, if you do not have metadata you will have to guess. 
    # These factors provide the possible options for the image size.
    print("Factors: " + str(factors(len(images))))
    

def factors(n):
    return set(reduce(
        list.__add__,
        ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
    
def main():
        lif_other = "IHC Cohort 2 6-4-25.lif"
        # display_lif(url,8,6)
        # lif_array = lif_to_np_array(url,8,6)
        
        # analyze_lif(lif_array)
    
        lifext = "IHC Cohort 2 5-27-25.lifext"
        lif = "IHC Cohort 2 5-27-25.lif"
        
        # print(get_count_images(lif_other))
        # count = get_count_images(lif)
        # print(factors(count))   
        display_individual_frames(lif,13,3)
        

if __name__ == "__main__":
    main()