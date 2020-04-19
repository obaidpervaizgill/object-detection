#from output.SaveTrafficObjects import SaveTrafficObjects

#test = SaveTrafficObjects()
#test.save()

from engine.DetectBeachObjects import DetectBeachObjects
if __name__ == "__main__":
    test = DetectBeachObjects()
    print(test.df_detect_all())
