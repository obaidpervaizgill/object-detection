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
import logging


class detectTrafficObjects(getTrafficData, columns, context):

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
        try:
            data = pd.DataFrame(map(lambda l: self.detect(l), self.to_detect_links()))
        except Exception as e:
            logging.error('Error opening data', exc_info=e)
        data[self.count] = data["label"].apply(lambda l: Counter(l))
        data_out = data.join(data["count"].apply(pd.Series).fillna(0))
        data_out[self.href] = data_out[self.href].astype(str)
        return data_out

    def save(self):
        data_one = self.df_detect_all()
        data_two = getTrafficData().df_all()
        data_out = data_one.merge(data_two, left_on=self.href, right_on=self.href)
        return data_out.to_csv('traffic_{}.csv'.format(datetime.now().strftime('%y%m%d-%H%M')), index=False)

