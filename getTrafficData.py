import requests as re
import json as jn
import pandas as pd
from columns import columns
from api import api

class getTrafficData:

    def __init__(self):
        super().__init__()

    def return_json(self):
        r = re.get(api.api_url, headers={"Authorization": api.auth_key})
        j = jn.loads(r.text)
        return j

    def json_to_df(self):
        data = pd.DataFrame(self.return_json()['features'])
        data_geo = pd.DataFrame.from_records(data['geometry'].values)
        data_prop = pd.DataFrame.from_records(data['properties'].values)
        data_out = {"geo": data_geo, "prop": data_prop}
        return data_out

    def df_links(self):
        data = self.json_to_df()["prop"]
        links = data[columns.href]
        num_links = len(links)
        return {"num_links": num_links, "links": links}

    def df_all(self):
        data_out = pd.DataFrame.join(self.json_to_df()["geo"], self.json_to_df()["prop"])
        data_out[columns.href] = data_out[columns.href].astype(str)
        return data_out
