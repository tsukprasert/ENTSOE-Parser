'''
calculate carbon intensity
'''

import re
import pandas as pd
import tabulate
import json 
import copy


class Calculation: 
    def __init__(self, filelist, countrylist, countrycodelist, eFactorFile): 
        self.filelist = filelist
        self.countries = countrylist
        self.countryCode = countrycodelist
        self.eFactorFile = eFactorFile
        
        self.columns = ["Biomass", "Coal", "Gas", "Geothermal", "Hydro", "Nuclear", "Oil", "Solar", "Wind", "Other"]

        self.emissionJSON = self.readeFactorFile()
        self.defaulteFactors = self.eFactorDefault()
        self.countryeFactors = self.overrideeFactors()
        self.dfList = self.generateDFList(filelist)
        self.calcDFList = self.processColumns() #list of DF with average intensity, this should be the last step

        #all in MWH


    def generateDFList(self, filelist): 
        dfList = []
        for file in filelist: 
            # print(file)
            df = pd.read_csv(file)
            df = df.iloc[: , 1:]
            df = df.replace('n/e', 0)
            df = df.replace('N/A', 0)
            df.columns = df.columns.str.strip()
            dfList.append(df)
        # print(dfList[0].head().to_markdown())
        return dfList 
    
    def processColumns(self): 
        # columns = self.columns

        '''
        Plan is to get the override library at some other function 
        '''
        groupedDF = []
        columns = self.columns 
        for index, dataframe in enumerate(self.dfList):
            # k = 1  

            # print(self.self.countries[index], self.countryCode[index])

               
            newDF = pd.DataFrame()

            biomass = dataframe["Biomass  - Actual Aggregated [MW]"] + dataframe["Waste  - Actual Aggregated [MW]"]
            coal = dataframe["Fossil Brown coal/Lignite  - Actual Aggregated [MW]"] + dataframe["Fossil Hard coal  - Actual Aggregated [MW]"] + dataframe["Fossil Oil shale  - Actual Aggregated [MW]"] + dataframe["Fossil Peat  - Actual Aggregated [MW]"]
            gas = dataframe["Fossil Coal-derived gas  - Actual Aggregated [MW]"] + dataframe["Fossil Gas  - Actual Aggregated [MW]"]
            geo = dataframe["Geothermal  - Actual Aggregated [MW]"]
            hydro = dataframe["Hydro Run-of-river and poundage  - Actual Aggregated [MW]"] + dataframe["Hydro Water Reservoir  - Actual Aggregated [MW]"]
            nuclear = dataframe["Nuclear  - Actual Aggregated [MW]"]
            oil = dataframe["Fossil Oil  - Actual Aggregated [MW]"]
            solar = dataframe["Solar  - Actual Aggregated [MW]"]
            wind = dataframe["Wind Offshore  - Actual Aggregated [MW]"] + dataframe["Wind Onshore  - Actual Aggregated [MW]"]
            other = dataframe["Other  - Actual Aggregated [MW]"] + dataframe["Other renewable  - Actual Aggregated [MW]"] + dataframe["Marine  - Actual Aggregated [MW]"]

            newDF["Biomass"] = biomass.astype('float64')
            newDF["Coal"] = coal.astype('float64')
            newDF["Gas"] = gas.astype('float64')
            newDF["Geothermal"] = geo.astype('float64')
            newDF["Hydro"] = hydro.astype('float64')
            newDF["Nuclear"] = nuclear.astype('float64')
            newDF["Oil"] = oil.astype('float64') 
            newDF["Solar"] = solar.astype('float64')
            newDF["Wind"] = wind.astype('float64')
            newDF["Other"] = other.astype('float64')

            #MWH to kWH
            newDF["Total kWH"] = newDF[columns].sum(axis=1, numeric_only=True) * 1000

            # print(newDF.head().to_markdown())

            self.calcCarbon(newDF, index)
            newDF['Total CO2eq'] = newDF[columns].sum(axis=1, numeric_only=True)
            
            # print("NEW")
            # print(newDF.head().to_markdown())

            self.calcAvg(newDF)
            # print("WITH AVG")
            # print(newDF.head().to_markdown())
            
            # newDF[]
            # #TODO: comeback here later 
            
            groupedDF.append(newDF)
        return groupedDF
    
    def calcCarbon(self, df, index):
        # print(self.countryeFactors)
        # print(df.head().to_markdown()) 
        df["Biomass"] = self.countryeFactors[self.countries[index]]['biomass'] * df["Biomass"] * 1000
        df["Coal"] = self.countryeFactors[self.countries[index]]['coal'] * df["Coal"] * 1000
        df["Gas"] = self.countryeFactors[self.countries[index]]['gas'] * df["Gas"] * 1000
        df["Geothermal"] = self.countryeFactors[self.countries[index]]['geothermal'] * df["Geothermal"]  * 1000
        df["Hydro"] = self.countryeFactors[self.countries[index]]['hydro'] * df["Hydro"] * 1000
        df["Nuclear"] = self.countryeFactors[self.countries[index]]['nuclear'] * df["Nuclear"] * 1000
        df["Oil"] = self.countryeFactors[self.countries[index]]['oil'] * df["Oil"] * 1000
        df["Solar"] = self.countryeFactors[self.countries[index]]['solar'] * df["Solar"] * 1000
        df["Wind"] = self.countryeFactors[self.countries[index]]['wind'] * df["Wind"] * 1000
        df["Other"] = self.countryeFactors[self.countries[index]]['unknown'] * df["Other"] * 1000
        
        

    def calcAvg(self, df): 
        df['Average'] = df['Total CO2eq'] / df['Total kWH']

    def readeFactorFile(self): 
        file = open(self.eFactorFile, 'r')
        emissionJSON = json.load(file)

        return emissionJSON
    
    def eFactorDefault(self):
        defaultDict = self.emissionJSON['emissionFactors']['defaults']
        sources = defaultDict.keys() #list of sources 
        defaultVal = dict()
        for source in sources: 
            try: 
                defaultVal[source] = defaultDict[source]['value']
                # print(source, defaultDict[source]['value'])
            except: 
                defaultVal[source] = defaultDict[source][-1]['value']
                # print(source, defaultDict[source][-1]["value"])

        return defaultVal

    def overrideeFactors(self): 
        overrideDict = self.emissionJSON['emissionFactors']['zoneOverrides']
        self.countryeFactors = dict()
        for index, countrycode in enumerate(self.countryCode): 
            # k = 1
            # print(countrycode)
            countryFactors = copy.deepcopy(self.defaulteFactors)
    # # # print("before update",countrycode,countryFactors)

    # # # print(countryFactors
            overrideFactors = overrideDict[countrycode].keys()
            for newfactor in overrideFactors:
    #             # print(newfactor, overrideDict[countrycode][newfactor][-1]['value'])
                try:
                    countryFactors[newfactor] = overrideDict[countrycode][newfactor][-1]['value']
                except: 
                    countryFactors[newfactor] = overrideDict[countrycode][newfactor]['value']
            self.countryeFactors[self.countries[index]] = countryFactors


        return self.countryeFactors

        
        # print(file)
       



if __name__ == "__main__":
    calc = Calculation(['/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_2021/Germany_2021.csv'], ['Germany'], ["DE"], "/Users/thanathorn/Desktop/map/timeslice_oop_Europe/default_docs/emissionFactors.json")
    # print(calc.calcDFList)
    # print(calc.countryeFactors)