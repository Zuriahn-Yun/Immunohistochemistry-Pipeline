from analyze import get_rgb
from readlif.reader import LifFile
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def analyze_lif(file_path):
    try:
        lif_file = LifFile(file_path)
        
        """ Display How many Images """
        image_count = lif_file
        print(image_count)
        
        """ Retrieve a frame from the lif image """
        lif_image = lif_file.get_image(0)
        pil_image = lif_image.get_frame(z=0)
        
        """ Convert to numpy array """
        np_image = np.array(pil_image)
        print(np_image.shape)
        
        """ Display Image """
        fig = px.imshow(np_image)
        fig.show()        
         
    except Exception as e:
        print('Error: ' + str(e))

def display_lif(file_path):
    
    lif = LifFile(file_path)
    fig = go.Figure()
    
    for image in lif.get_iter_image():
        for frame in image.get_iter_image():
            
            arr = np.array(frame)
            fig.add_layout_image(
                px.imshow(image)
            )
            
    fig.show()



def main():
        url = "IHC Cohort 2 6-4-25.lif"
        display_lif(url)

if __name__ == "__main__":
    main()