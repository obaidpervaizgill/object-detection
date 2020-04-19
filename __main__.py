#from output.SaveTrafficObjects import SaveTrafficObjects

#test = SaveTrafficObjects()
#test.save()
from input.GetBeachData import GetBeachData
if __name__ == "__main__":
    test = GetBeachData()
    print(test.timestamps_to_df())
