import numpy as np
import urllib
import cv2
import ssl
import cvlib as cv
from cvlib.object_detection import draw_bbox
from datetime import datetime
import logging
from columns import columns
from getData import getData

class detectObjects(columns, getData):

    def __init__(self):
        self.links = getData.df_links()


