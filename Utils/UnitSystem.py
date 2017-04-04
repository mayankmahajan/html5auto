import math
import decimal
from Utils.logger import *
from Utils.resultlogger import *


class UnitSystem :
    def __init__(self):
        pass
    metricUnits = ["", "K", "M", "B", "T", "P", "E", "Z", "Y"]
    metricValues = [1,1000,1000,1000,1000, 1000, 1000, 1000, 1000]
    #byteUnits = ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]
    #metricUnits= ["", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    byteUnits = ["", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    byteValues = [1,1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024]
    timeUnits = ["s","m"]
    timeValues = [1,"60"]

    '''
    def getRawValue(self,convertedValue,unitString):
        convertedValue = float(convertedValue)
        if "bps" in unitString:
            unit = unitString.strip('bps')
            rawValue = convertedValue*self.byteValues[self.byteUnits.index(unit)]**self.byteUnits.index(unit)
        elif unitString in self.metricUnits:
            rawValue = convertedValue*self.metricValues[self.metricUnits.index(unitString)]**self.metricUnits.index(unitString)
        elif unitString in self.timeUnits: # for handle timeunit
            rawValue = convertedValue*self.timeValues[self.timeUnits.index(unitString)]
        else:  # avoid exception for unit other than above units
            logger.info("%s Unit not present in unit system hence retrun 0.0",unitString)
            rawValue=0.0
        return rawValue
    '''

    # updated unit system
    def getRawValue(self, convertedValue, unitString):
        if unitString =="":
            return convertedValue

        convertedValue = float(convertedValue)
        if unitString in self.timeUnits:
            rawValue = convertedValue * self.timeValues[self.timeUnits.index(unitString)]
        elif unitString in self.byteUnits or "bps" in unitString:
            if "bps" in unitString:
                unit=unitString.strip('bps')+"B"
            else:
                unit=unitString
            rawValue = convertedValue * self.byteValues[self.byteUnits.index(unit)] ** self.byteUnits.index(unit)
        elif unitString in self.metricUnits:
            rawValue = convertedValue * self.metricValues[self.metricUnits.index(unitString)] ** self.metricUnits.index(unitString)
        else:
            logger.info("%s Unit not present in unit system hence retrun 0.0", unitString)
            rawValue = 0.0
        return rawValue

    def getValueFromRawValue(self,convertedValue,unitValue=1024.0,unitstring=""):

        convertedValue=float(convertedValue)
        unitValue=float(unitValue)
        if unitValue == 60.0:
            return str(int(convertedValue))+ " "+'s'  # assume time in sec only ( s=>m Conversion not applied here)
        count=0
        while (convertedValue / unitValue) > unitValue:
            convertedValue = convertedValue / unitValue
            count = count + 1
        if convertedValue>unitValue:
            convertedValue = convertedValue / unitValue
            count = count+1

        a = decimal.Decimal(str(convertedValue))
        if unitValue == 1000.0:
            return str(round(a, 2)) + " " + self.metricUnits[count]
        elif unitValue== 1024.0 and "bps" in unitstring:
            return str(round(a, 2))+ " "+ (self.byteUnits[count]).strip('B') +"bps"
        else:
            return str(round(a, 2)) + " " + self.byteUnits[count]



    def getRawValueFromUI(self,uiValue):
        import re
        vArr =  re.findall('[0-9]+',uiValue)
        if len(vArr) ==1 :
            value = float(vArr[0])
        elif len(vArr) ==2:
            value = float(str(vArr[0]+"."+vArr[1]))

        if len(re.findall(r'[a-zA-Z]+',uiValue))==0:
            unitstring=""
        else:
            unitstring = str(re.findall(r'[a-zA-Z]+',uiValue)[0])

        return self.getRawValue(value,unitstring)





