from ast import fix_missing_locations
from hashlib import new
from re import S
from tkinter import Y
import matplotlib.pyplot as plt
import numpy as np
# from itertools import permutations

class Yearly: 
    def __init__(self, yearlyDFList, countryList, year, showPlot): 
        self.yearlyDFList = yearlyDFList
        self.countries = countryList
        self.showPlot = showPlot
        self.year = year
        
        if(self.showPlot):
            self.yearlyPlot()

    def yearlyPlot(self): 
        plt.figure()
        for newdata in self.yearlyDFList:
            plt.plot(newdata['Average'])
        plt.axhline(y=200, xmin=0, xmax=23, color='g')
        plt.axhline(y=400, xmin=0, xmax=23, color='y')
        plt.axhline(y=600, xmin=0, xmax=23, color='brown')
        plt.legend(self.countries)
        plt.grid()
        # plt.xticks(np.arange(0, 8760, 730))
        plt.title(self.year)
        plt.ylabel("Average Carbon Intensity (gCO2eq/kHh)")
        # plt.xlabel("")
        plt.tight_layout()
        plt.show()



class Monthly: 
    def __init__(self, yearlyDFList, countryList, year, showPlot): 
        self.yearlyDFList = yearlyDFList
        self.countries = countryList
        self.year = year
        self.showPlot = showPlot
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
        self.monthlist = []
        self.monthrows = dict()
        self.monthbounds = dict()
        self.monthlyDFDict = dict() 

        # add stuff below here, the top part is set 

        self.permutations = []
        self.xAxis = []

        self.init()
        self.monthlyPlot()
        # print(len(self.monthlyDFDict["Jan"])) 


    def init(self):
        self.initrowcount()
        self.initbounds()

    def initrowcount(self):
        if(self.year % 4 == 0): 
            self.yearDict["Feb"] = 29
        # print(self.yearDict)
        for month, days in self.yearDict.items(): 
            self.monthlist.append(month)
            self.monthrows[month] = days*self.oneday

    def initbounds(self): 
        for key, item in self.monthrows.items():
            if(key == "Jan"): 
                lower = 0 
                upper = item 
            else: 
                lower = upper 
                upper += item 
            self.monthbounds[key] = (lower, upper)

    def monthlyPlot(self): 
        self.generatePermutation()
        self.generateMonthlyDF()
        self.formatAxis()

        if(self.showPlot):
            self.plotMonths()
        # for df in self.yearlyDFList: 
        #     print(df.shape)

    def generateMonthlyDF(self): 
        for i in range(self.month): 
            lower = self.monthbounds[self.monthlist[i]][0]
            upper = self.monthbounds[self.monthlist[i]][1]
            month = self.monthlist[i]
            self.monthlyDFDict[month] = []
            for df in self.yearlyDFList:
                newDF = df.iloc[lower:upper, :]
                # print(i, newDF.shape)
                self.monthlyDFDict[month].append(newDF)
        # print(len(self.monthlyDFDict["Jan"]))

    def generatePermutation(self): 
        for r in range(self.row): 
            for c in range(self.column): 
                self.permutations.append((r,c))

    def formatAxis(self):

        for month in self.monthlist:
            newlist = []
            size = self.monthlyDFDict[month][0].shape[0]
            for i in range (size//24): 
                for j in range(24): 
                    newlist.append(j)
            # newlist = np.arange(0, size, 24)
            # print(newlist)
            # break
            self.xAxis.append(newlist)

        #     # newlist = []
        #     newlist = np.arange(0, , 24): 


        # for monthlyDF in monthlyDF
        # self.xAxis = np.linspace(0, upper, upper)
        # print(self.xAxis)

    def plotMonths(self): 
        fig, axs = plt.subplots(self.row, self.column, figsize=(20,10), sharey=True)
        fig.suptitle(self.year)
        # plt.xticks(self.xAxis[index])
        # print()

        for month, monthList in self.monthlyDFDict.items(): 
            index = self.monthIndex[month]
            # print(self.permutations[index])
            subplot = axs[self.permutations[index]]
            subplot.title.set_text(month)
            # subplot.xaxis.set_ticks(self.xAxis[index])
            

            # axs.set_xticklabels()

            # print(len(monthList))
                
            for df in monthList:
                # print(month, df.shape)
                subplot.plot(df["Average"])
            # plt.xticks(self.xAxis[index])
                # 

            
        # # #     # print(month, self.monthIndex[month]) 
        # axs.set_ylabel("Average Carbon Intensity (gCO2eq/kHh)")
        # axs.set_xlabel("Hour")
        plt.legend(self.countries,bbox_to_anchor=(1,1), loc="upper left" )
        plt.tight_layout()
        plt.show()







#---------------------------------------- Class Global Varibles ----------------------------------------
    oneday = 24 # hours
    month = 12

    row = 3 
    column = 4

    monthIndex = {
        "Jan": 0,
        "Feb": 1,
        "Mar": 2,
        "Apr": 3,
        "May": 4,
        "Jun": 5,
        "Jul": 6,
        "Aug": 7,
        "Sep": 8,
        "Oct": 9,
        "Nov": 10,
        "Dec": 11

    }



class Daily: 
    def __init__(self, month, monthlyDFDict, year, countryList, showPlot): 
        self.month = month # month to be plotted 
        self.monthDFDict = monthlyDFDict
        self.monthDFList = monthlyDFDict[month]

        self.countries = countryList
        # print(countryList)
        self.year = year
      
        self.showPlot = showPlot

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
        self.checkleapyear()
        
        self.days =  self.yearDict[month]
        self.permutations = []
        self.dailybounds = []
        self.dailyDFDict = dict()
        self.ticks = []

        #remove case is 31 (4*8 = 32)
        self.row = 4
        self.column = 8


       
        self.init(self.days)
        
        self.dailyPlot(self.month, self.monthDFList) 

    def checkleapyear(self): 
        if(self.year % 4 == 0):
            self.yearDict["Feb"] = 29

    def init(self, days): 

        for d in range(days): 
            if d == 0: 
                lower = 0 
                upper = 24
            else:
                lower = upper 
                upper += 24
            self.dailybounds.append((lower, upper))

        # print(self.dailybounds)
        # # for df in self.monthDFList: 
        # #     print(df.shape)
        # #     break


    def dailyPlot(self, month, monthdfList):
        days = self.days
        self.generatePermutation(days)
        self.setticks()
        self.generateDailyDF()


        if(self.showPlot): 
            self.plotDays()
    
    def generatePermutation(self, days):
        
        toRemove = self.setRowColumn(days)

        for r in range(self.row): 
            for c in range(self.column): 
                self.permutations.append((r,c))
            
        if(toRemove): 
            self.permutations = self.permutations[:-1]
    
    def setRowColumn(self, days): 
        remove = True
        if(days == 30 or days == 29): 
            self.row = 5 
            self.column = 6

            if(days == 30): 
                remove = False

        elif(days == 28): 
            self.column = 7 
            remove = False
        
        return remove

    def generateDailyDF(self): 
        for i in range(self.days): 
            lower = self.dailybounds[i][0]
            upper = self.dailybounds[i][1]
            self.dailyDFDict[i] = []

            for df in  self.monthDFList: 
                newDF = df.iloc[lower:upper, :]
                # print(newDF.shape)
                self.dailyDFDict[i].append(newDF)
    
    def plotDays(self): 
        
        fig, axs = plt.subplots(self.row, self.column, figsize=(20,10), sharey=True)
        # fig.set_yticklabels(fontsize=7)
       
        # plt.setp(axs, xticks=self.ticks)
        for day, dayList in self.dailyDFDict.items(): 
            # print(day, len(dayList))

            index = day 
            subplot = axs[self.permutations[index]]
            subplot.title.set_text(index+1)
          
            # subplot.set_yticklabels(fontsize=7)
            # subplot.tick_params(axis='x', rotation=90)
            # subplot.set_xticks(self.ticks)
            for df in dayList: 
                subplot.plot(self.ticks, df['Average'])
            
            # subplot.grid()
    
    
            
        # plt.legend()
        # plt.legend(self.countries,loc="best" )
        # plt.export_legend(legend)
        fig.legend(self.countries)
        # fig.grid()
        fig.suptitle(self.month)

        plt.tight_layout()
        plt.show()
 
    def setticks(self): 
        for i in range(24): 
            self.ticks.append(i)

class OneDay: 
    def __init__(self, month, date, year, monthlyDFDict, countryList, showPlot): 
        self.month = month 
        self.date = date 
        self.year = year 
        self.monthDFDict = monthlyDFDict
        self.monthDFList = monthlyDFDict[month]
        self.countries = countryList
        self.showPlot = showPlot


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
        self.ticks = []
        self.dailybounds = []
        self.days = self.yearDict[month]
        self.checkleapyear()

       
        self.init(self.days)        

        self.bound = self.dailybounds[self.date] 
        self.oneDayDFList = []
        self.generateOneDayDF()


        if(self.showPlot): 
            self.plotOneDay()

    def checkleapyear(self): 
        if(self.year % 4 == 0):
            self.yearDict["Feb"] = 29

    def init(self, days): 
        for d in range(days): 
            if d == 0: 
                lower = 0 
                upper = 24
            else:
                lower = upper 
                upper += 24
            self.dailybounds.append((lower, upper))
        
        self.setticks()
    
    def setticks(self):
        for i in range(24): 
            self.ticks.append(i)

    def generateOneDayDF(self):
        lower = self.bound[0]
        upper = self.bound[1]
        for df in self.monthDFList: 
            newDF = df.iloc[lower:upper, :]
            self.oneDayDFList.append(newDF)

        
    def plotOneDay(self):
        title = "Average Carbon Intensity %s %s, %s"%(self.month, self.date, self.year)
        plt.figure()

        for df in self.oneDayDFList:
            plt.plot(self.ticks, df['Average'])

        plt.legend(self.countries)
        plt.title(title)
        plt.ylabel("Average Carbon Intensity (gCO2eq/kHh)")
        plt.xlabel("Hour")
        plt.grid()
        plt.xticks(self.ticks)
        # manager = plt.get_current_fig_manager()
        # manager.full_screen_toggle()
        

        plt.tight_layout()
        plt.show()



