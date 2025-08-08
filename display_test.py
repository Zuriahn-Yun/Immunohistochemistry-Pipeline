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
Quantify red signal area, intensity distribution
Identify colocalization regions (red AND blue above thresholds)
Generate metrics like overlap coefficients, Manders' coefficients
"""