'''
takes care of the global stuff, to be accessed globally 

file should be formatted as Countryname_year.csv
'''
import os
import json

class Global: 
    def __init__(self, dirpath, year, countrycodepath): 
        self.dirpath = dirpath
        self.year = year
        self.countrycodefile = countrycodepath
        self.files = self.list_full_paths(dirpath)
        self.entsoecode = self.entsoeCode() # dictionary containing electricity map country code

        self.countries = self.countryList()
        self.countryCode = self.countryCodeList()


        self.yearDict = {

                "Jan": 31,
                "Feb": 28,
                "Mar": 31,
                "Apr": 30,
                "May": 31,
                "Jun": 30,
                "Jul": 31,
                "Aug": 31,
                "Sep": 30,
                "Oct": 31,
                "Nov": 30,
                "Dec": 31
        }

        self.monthList = []
        self.monthListSetup()
    
    def list_full_paths(self, directory):
        return [os.path.join(directory, file) for file in os.listdir(directory)]
    
    def countryList(self): 
        countries = []
        for filepath in self.files: 
            filename = filepath.split('/')[-1]
            countryname = filename.split('_')[0]
            countries.append(countryname)
        return countries
            

    
    def countryCodeList(self): 
        countrycodes = []
        for country in self.countries: 
            countrycodes.append(self.entsoecode[country])

        return countrycodes

    def entsoeCode(self):  
        f = open(self.countrycodefile, 'r')
        return json.load(f)

    def monthListSetup(self): 
        for month in self.yearDict.keys(): 
            self.monthList.append(month)

if __name__ == "__main__":
    dir = Global("/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_2021", 2021, "timeslice_oop_Europe/default_docs/entsoe_code.json")
    print(dir.files)
    # print(dir.countries)
    # print(dir.countryCode)
