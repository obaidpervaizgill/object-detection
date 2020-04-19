from utilities.Columns import Columns
from input.GetBeachData import GetBeachData
from engine.DetectTrafficObjects import DetectTrafficObjects
from PIL import Image
from urllib.request import urlopen
from urllib.parse import urlparse
from datetime import datetime
from collections import Counter
import cvlib as cv
import numpy as np
import pandas as pd


class DetectBeachObjects(GetBeachData, DetectTrafficObjects):

    def __init__(self):
        super().__init__()
        self.all = False
        self.length = 10

    def to_detect_links(self):
        if self.all:
            link_all = [l for l in self.timestamps_to_df()["links"] if urlparse(l)]
        else:
            link_all = [l for l in self.timestamps_to_df()["links"] if urlparse(l)][:self.length]
        return link_all

    def detect(self, url):
        req_url = Image.open(urlopen(url))
        image = np.array(req_url.convert('RGB'))
        bbox, label, conf = cv.detect_common_objects(image)
        return {"href": url,
                "label": label,
                "confidence": conf,
                "box": bbox,
                "time": [datetime.now().strftime("%Y/%m/%d-%H:%M:%S")]}

