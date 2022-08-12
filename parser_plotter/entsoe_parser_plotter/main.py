from audioop import avg
from math import fabs
import os 
import setup, processdata, calculation, plotting
import matplotlib.pyplot as plt


if __name__ == "__main__":
    print(__file__)
    
    #use absolute paths
    dirpath = "/Users/thanathorn/Desktop/ENTSOE Parser/parser_plotter/yearly_data_2021"
    entsoecode = "/Users/thanathorn/Desktop/ENTSOE Parser/parser_plotter/entsoe_parser_plotter/default_docs/entsoe_code.json"
    eFactorFile = "/Users/thanathorn/Desktop/ENTSOE Parser/parser_plotter/entsoe_parser_plotter/default_docs/emissionFactors.json"
    year = 2021
    
    dir = setup.Global(dirpath, year, entsoecode)
    
    #make sure that all the data is in the same format 
    dataclean = processdata.ProcessData(dir.dirpath, dir.files)

    avgdata = calculation.Calculation(dir.files, dir.countries, dir.countryCode, eFactorFile)

    yearlyPlot = plotting.Yearly(avgdata.calcDFList, dir.countries, year, showPlot=False)
    monthlyPlot = plotting.Monthly(avgdata.calcDFList, dir.countries, year, showPlot=False)

    for month in dir.yearDict.keys(): 
        newplot = plotting.Daily(month,monthlyPlot.monthlyDFDict, 2021, dir.countries, showPlot=True)
    # plt.show()
        # print(month)
    # dailyPlot = plotting.Daily("Mar",monthlyPlot.monthlyDFDict, 2021, dir.countries, showPlot=True)
    onedayPlot = plotting.OneDay("Mar", 9, 2021, monthlyPlot.monthlyDFDict, dir.countries, showPlot=False)


    plt.show()