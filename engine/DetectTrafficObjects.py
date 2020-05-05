from utilities.Columns import Columns
from utilities.Context import Context
from utilities.Yolo import Yolo
from input.GetTrafficData import GetTrafficData
from urllib import request
from urllib.parse import urlparse
from datetime import datetime
from collections import Counter
import cv2
import os
import cvlib as cv
import numpy as np
import pandas as pd


class DetectTrafficObjects(GetTrafficData, Context, Yolo):

    def __init__(self):
        self.all = False
        self.length = 3
        self.data_key = self.href
        self.out_path = os.getcwd()
        self.out_folder = "/output/"
        self.file_name = "traffic"

    def to_detect_links(self):
        if self.all:
            link_all = [l for l in self.df_links()["links"] if urlparse(l)]
        else:
            link_all = [l for l in self.df_links()["links"] if urlparse(l)][:self.length]
        return link_all

    def detect(self, url):
        req_url = request.urlopen(url)
        image = np.asarray(bytearray(req_url.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        bbox, label, conf = cv.detect_common_objects(image, confidence=self.confidence, model=self.model)
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

    def save(self):
        data_out = self.df_all().merge(self.df_detect_all(), on=self.data_key, how="inner")
        return data_out.to_csv(
            self.out_path + self.out_folder + self.file_name + r'{}.csv'.format(datetime.now().strftime('%y%m%d-%H%M')))
