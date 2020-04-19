from datetime import datetime
from datetime import timedelta
import pandas as pd
import os
from utilities.Api import Api
from utilities.Columns import Columns


class GetBeachData(Api, Columns):
    def __init__(self):
        self.twenty_four_hours = 2400
        self.look_back_day = 1
        self.minute_increment = 10
        self.minute_parse = -2
        self.min_limit = 50
        self.in_path = os.getcwd()
        self.in_folder = "/input/"
        self.file_name = "beach"

    def return_timestamps(self):
        hours = ["%04d" % h for h in range(0, self.twenty_four_hours) if (h % self.minute_increment == 0)]
        days = [(datetime.now() - timedelta(days=d)).strftime('%Y%m%d') for d in
                range(0, self.look_back_day + 1)]
        timestamp = [(d + h) for d in days for h in hours if int((d + h)[self.minute_parse:]) <= self.min_limit]
        return timestamp

    def df_links(self):
        data_out = pd.concat(
            [pd.DataFrame(
                {"cameras": [l], "links": [self.api_url_beach.format(l, t)], "daytime": [t]}
            )
                for l in self.api_location_beach.values()
                for t in self.return_timestamps()
            ]
        )
        return data_out

    def df_all(self):
        data_in = pd.read_csv(self.in_path + self.in_folder + r'{}.csv'.format(self.file_name))
        data_in[self.cameras] = data_in[self.cameras].astype(str)
        data_out = self.df_links().merge(data_in, on=self.cameras, how="left")
        data_out = data_out.rename(columns={"links": self.href})
        return data_out
