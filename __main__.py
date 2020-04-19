from engine.DetectBeachObjects import DetectBeachObjects
from engine.DetectTrafficObjects import DetectTrafficObjects
if __name__ == "__main__":
    beach = DetectBeachObjects()
    traffic = DetectTrafficObjects()
    beach.save()
    traffic.save()
