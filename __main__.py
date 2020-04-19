#from output.SaveTrafficObjects import SaveTrafficObjects

#test = SaveTrafficObjects()
#test.save()

from engine.DetectBeachObjects import DetectBeachObjects
if __name__ == "__main__":
    test = DetectBeachObjects()
    sample = test.timestamps_to_df()["links"].tolist()[90]
    print(test.df_detect_all())
    #print(test.to_detect_links())
