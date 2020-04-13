from detectTrafficObjects import detectTrafficObjects
from getTrafficData import getTrafficData
from columns import columns
import os
import logging
from datetime import datetime

class saveTrafficObjects(detectTrafficObjects):
    def __init__(self):
        super().__init__()
        self.out_path = os.getcwd()
        self.out_folder = "output"
        self.file_name = "traffic"

    def save(self):
        data_out = self.df_detect_all().merge(getTrafficData().df_all(), left_on=columns.href, right_on=columns.href)
        return data_out.to_csv(os.path.join(self.out_path,r'output/traffic_{}.csv'.format(datetime.now().strftime('%y%m%d-%H%M'))))
