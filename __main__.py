from detectTrafficObjects import detectTrafficObjects

if __name__ == "__main__":
    test = detectTrafficObjects()
    print (test.df_detect_all().head())