from columns import columns
from context import context
from getTrafficData import getTrafficData
from urllib import request
from urllib.parse import urlparse
import cv2
import cvlib as cv
import numpy as np
import logging


class detectTrafficObjects(getTrafficData, columns, context):

    def __init__(self):
        super().__init__()

    def to_detect(self, all=True, length=3):
        if all:
            link_all = getTrafficData().df_links()["links"]
        else:
            link_all = getTrafficData().df_links()["links"][:length]
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
        return {"label": label, "confidence": conf, "box": bbox}

    def detect_all(self):
        data_out = list(map(lambda l: self.detect(l), self.to_detect(False)))
        return data_out

    def detect_all_label(self):
        pass



if __name__ == "__main__":
    test = detectTrafficObjects()
    # print(test.detect(test.link_all))
    print (test.detect_all())
    #print (test.to_detect(False,3))
