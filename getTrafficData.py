import requests as re
import json as jn
import pandas as pd
import logging
from columns import columns
from api import api

class getTrafficData(api, columns):

    def __init__(self):
        super().__init__()

    def return_json(self):
        try:
            r = re.get(self.api_url, headers={"Authorization": self.auth_key})
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

    def df_links(self):
        try:
            data = self.json_to_df()["prop"]
        except Exception as e:
            logging.error('Error at extracting links to data frame'.format(data.shape), exc_info=e)
        links = data[self.href]
        num_links = len(links)
        return {"num_links": num_links, "links": links}

    def df_all(self):
        try:
            data_out = pd.DataFrame.join(self.json_to_df()["geo"], self.json_to_df()["prop"])
            data_out[self.href] = data_out[self.href].astype(str)
        except Exception as e:
            logging.error('Error at joining data frames'.format(data_out.shape), exc_info=e)
        return data_out
