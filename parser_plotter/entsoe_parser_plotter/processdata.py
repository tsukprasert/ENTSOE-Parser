'''
After getting the data in the folder, check the format first

'''
from time import time
import pandas as pd 
import os
from requests import head
import tabulate
import csv

class ProcessData: 
    def __init__(self, dirpath, filelist): 
        self.dirpath = dirpath
        self.files = filelist 
        self.checkformat()
        self.dataframes = self.process()
    
    def checkformat(self): 
        for file in self.files: 
            df = pd.read_csv(file)
            timeinterval = df["MTU"][0].split('-')[1].split()[1].split(":")[1] #check the first interval
            if(timeinterval == "15"): 
                self.processFile(file)
            # spaindata = spaindata.iloc[:, 2:]
            # spaindata = spaindata.replace('n/e', 0)
            # spaindata = spaindata.replace('N/A', 0)

    def processFile(self, filename):
        df = pd.read_csv(filename)
        df = df.iloc[:, 2:]
        df = df.replace('n/e', 0)
        df = df.replace('N/A', 0)

        timeinterval, countrycode = self.newInterval(filename)

        df_combine = df.groupby(df.index//4).mean()
        df_combine.insert(0, "Area",countrycode)
        df_combine.insert(1, "MTU",timeinterval)

        #remove and replace
        os.remove(filename)
        df_combine.to_csv(filename,encoding='utf-8', index=False)
        # print(df_combine.head().to_markdown())




        # print(len(timeinterval))


    def newInterval(self, filename): 
        header = dict()
        timeInterval = []
        countryCode = [] 
        with open(filename, 'r') as file: 
            file_obj = csv.reader(file)
            firstrow = next(file_obj)
            # print(firstrow)
            #associate column name and index number, for easy reference 
            for index, column in enumerate(firstrow): 
                header[column.strip()] = index

            for index, row in enumerate(file_obj): 
                if(index %4 == 0):
                    prev = index
                    firsthalf = row[header["MTU"]].split(' - ')[0]
                if(index == prev+3): 
                    secondhalf = row[header["MTU"]].split(' - ')[1]
                    interval = "%s - %s"%(firsthalf, secondhalf)#firsthalf, " - ",secondhalf
            # print(interval)
                    timeInterval.append(interval)
                    countryCode.append(row[header["Area"]])

        return timeInterval, countryCode
    
    def process(self): 
        dflist = []
        

        return dflist
                


if __name__ == "__main__":
    # print(__file__)
    # processdata = ProcessData(
    #     [
    #     '/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_2021/Germany_2021.csv',
    #     '/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_2021/Spain_2021.csv', 'Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_2021/Netherlands_2021.csv',
    #     '/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_2021/Finland_2021.csv', 
    #     '/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_2021/Switzerland_2021.csv', 
    #     '/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_2021/Poland_2021.csv', 
    #     '/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_2021/Belgium_2021.csv']
    #     )

    processdata = ProcessData("/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_testprocessing",[
        "/Users/thanathorn/Desktop/map/timeslice/yearly/yearly_data_testprocessing/Germany_2021.csv"
    ])