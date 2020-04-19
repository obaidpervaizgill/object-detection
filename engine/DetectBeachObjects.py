from input.GetBeachData import GetBeachData
from engine.DetectTrafficObjects import DetectTrafficObjects
from PIL import Image
from urllib.request import urlopen
from datetime import datetime
import cvlib as cv
import numpy as np


class DetectBeachObjects(GetBeachData, DetectTrafficObjects):

    def __init__(self):
        super().__init__()
        self.all = False
        self.length = 10

    def detect(self, url):
        req_url = Image.open(urlopen(url))
        image = np.array(req_url.convert('RGB'))
        bbox, label, conf = cv.detect_common_objects(image)
        return {"href": url,
                "label": label,
                "confidence": conf,
                "box": bbox,
                "time": [datetime.now().strftime("%Y/%m/%d-%H:%M:%S")]}

