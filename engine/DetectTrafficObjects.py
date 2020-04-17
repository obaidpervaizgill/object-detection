from utilities.Columns import Columns
from utilities.Context import Context
from input.GetTrafficData import GetTrafficData
from urllib import request
from urllib.parse import urlparse
from datetime import datetime
from collections import Counter
import cv2
import cvlib as cv
import numpy as np
import pandas as pd
import logging


class DetectTrafficObjects(GetTrafficData, Context):

    def __init__(self):
        self.all = True
        self.length = 3

    def to_detect_links(self):
        if self.all:
            link_all = self.df_links()["links"]
        else:
            link_all = self.df_links()["links"][:self.length]
        return link_all

    def detect(self, url):
        try:
            url_valid = urlparse(url)
        except Exception as e:
            logging.error('Error at opening url'.format(url_valid), exc_info=e)
        req_url = request.urlopen(url, context=self.context)
        image = np.asarray(bytearray(req_url.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
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
