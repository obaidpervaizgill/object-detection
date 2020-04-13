from columns import columns
from context import context
from getTrafficData import getTrafficData
from urllib import request
from urllib.parse import urlparse
from datetime import datetime
from collections import Counter
import cv2
import cvlib as cv
import numpy as np
import pandas as pd
import os
import logging


class detectTrafficObjects:

    def __init__(self):
        super().__init__()
        self.all = True
        self.length = 3

    def to_detect_links(self):
        if self.all:
            link_all = getTrafficData().df_links()["links"]
        else:
            link_all = getTrafficData().df_links()["links"][:self.length]
        return link_all

    def detect(self, url):
        try:
            url_valid = urlparse(url)
        except Exception as e:
            logging.error('Error at opening url'.format(url_valid), exc_info=e)
        req_url = request.urlopen(url, context=context.context)
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
        data[columns.count] = data["label"].apply(lambda l: Counter(l))
        data_out = data.join(data["count"].apply(pd.Series).fillna(0))
        data_out[columns.href] = data_out[columns.href].astype(str)
        return data_out
