from analyze import get_rgb
from readlif.reader import LifFile
import numpy as np

def analyze_lif(file_path):
    try:
        lif_file = LifFile(file_path)
        
        """ Display How many Images """
        image_count = lif_file
        print(image_count)
        
        
        lif_image = lif_file.get_image(0)
        pil_image = lif_file.get_frame(z=0)
        np_image = np.array(pil_image)
        np_image.shape
         
         
    except Exception as e:
        print('Error: ' + str(e))




def main():
        url = "IHC Cohort 2 6-4-25.lif"
        analyze_lif(url)

if __name__ == "__main__":
    main()