from utilities.Columns import Columns
from utilities.Context import Context
from input.GetBeachData import GetBeachData
from PIL import Image
from urllib.request import urlopen
from urllib.parse import urlparse
from datetime import datetime
from collections import Counter
import cv2
import cvlib as cv
import numpy as np
import pandas as pd
import logging


class DetectBeachObjects(GetBeachData):

    def __init__(self):
        super().__init__()
        self.all = False
        self.length = 100

    def to_detect_links(self):
        if self.all:
            link_all = [l for l in self.timestamps_to_df()["links"] if urlparse(l)]
        else:
            link_all = [l for l in self.timestamps_to_df()["links"] if urlparse(l)][:self.length]
        return link_all

    def detect(self, url):
        try:
            url_valid = urlparse(url)
        except Exception as e:
            logging.error('Error at opening url'.format(url_valid), exc_info=e)
        req_url = Image.open(urlopen(url))
        image = np.array(req_url.convert('RGB'))
        bbox, label, conf = cv.detect_common_objects(image)
        return {"href": url,
                "label": label,
                "confidence": conf,
                "box": bbox,
                "time": [datetime.now().strftime("%Y/%m/%d-%H:%M:%S")]}

    def df_detect_all(self):
        data = pd.DataFrame(map(lambda l: self.detect(l), self.to_detect_links()))
        data[self.count] = data["label"].apply(lambda l: Counter(l))
        data_out = data.join(data["count"].apply(pd.Series).fillna(0))
        data_out[Columns.href] = data_out[Columns.href].astype(str)
        return data_out
