import requests as re
import json as jn
import pandas as pd
import logging

class getData:

    def __init__(self):
        self.url = "https://api.transport.nsw.gov.au/v1/live/cameras"
        self.auth_key = "apikey gfD10KWo3RWoQrJBEyD85dnx2N7Pn2u68bWH"



    def return_json(self):
        try:
            r = re.get(self.url, headers={"Authorization": self.auth_key})
        except Exception as e:
            logging.error('Error at data pull from api'.format(r), exc_info=e)
        j = jn.loads(r.text)
        return j

    def json_to_df(self):
        try:
            data = pd.DataFrame(self.return_json()['features'])
        except Exception as e:
            logging.error('Error at data transformation from json to data frame'.format(data.shape), exc_info=e)
        data_geo = pd.DataFrame.from_records(data['geometry'].values)
        data_prop = pd.DataFrame.from_records(data['properties'].values)
        data_out = {"geo": data_geo, "prop": data_prop}
        return data_out

    def all_df(self):
        try:
            data_out = pd.DataFrame.join(self.json_to_df()["geo"], self.json_to_df()["prop"])
        except Exception as e:
            logging.error('Error at joining data frames'.format(data_out.shape), exc_info=e)
        data_out['index'] = data_out.index
        return data_out



