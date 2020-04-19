import os
from datetime import datetime
from engine.DetectTrafficObjects import DetectTrafficObjects


class SaveTrafficObjects(DetectTrafficObjects):

    def __init__(self):
        super().__init__()
        self.out_path = os.getcwd()
        self.out_folder = "/output/"
        self.file_name = "traffic"
        self.data_left = self.df_all()
        self.data_right = self.df_detect_all()
        self.data_key = self.href

    def save(self):
        data_out = self.data_left.merge(self.data_right, on=self.data_key, how="inner")
        return data_out.to_csv(
            self.out_path + self.out_folder + self.file_name + r'{}.csv'.format(datetime.now().strftime('%y%m%d-%H%M')))
