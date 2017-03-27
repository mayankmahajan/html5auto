import math
import decimal

class UnitSystem :
    def __init__(self):
        pass
    # metricUnits = ["", "K", "M", "B", "T", "P", "E", "Z", "Y"]
    metricValues = [1,1000,1000,1000,1000, 1000, 1000, 1000, 1000]
    byteUnits = ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]
    metricUnits= ["", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    byteValues = [1,1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024]
    timeUnits = ["s","m"]
    timeValues = [1,"60"]

    def getRawValue(self,convertedValue,unitString):
        convertedValue = float(convertedValue)
        if "bps" in unitString:
            unit = unitString.strip('bps')
            rawValue = convertedValue*self.byteValues[self.byteUnits.index(unitString)]**self.byteUnits.index(unitString)
        else:
            rawValue = convertedValue*self.metricValues[self.metricUnits.index(unitString)]**self.metricUnits.index(unitString)
        return rawValue

    def getValueFromRawValue(self,convertedValue,unitValue=1000.0):
        convertedValue=float(convertedValue)
        unitValue=float(unitValue)
        count=0
        while (convertedValue / unitValue) > unitValue:
            convertedValue = convertedValue / unitValue
            count = count + 1
        if convertedValue>unitValue:
            convertedValue = convertedValue / unitValue
            count = count+1

        a = decimal.Decimal(str(convertedValue))
        if unitValue == 1000.0:
            return str(round(a, 2))+ " "+ self.metricUnits[count]
        else:
            return str(round(a, 2)) + " " + self.byteUnits[count]+"bps"


    def getRawValueFromUI(self,uiValue):
        import re
        vArr =  re.findall('[0-9]+',uiValue)
        if len(vArr) ==1 :
            value = float(vArr[0])
        elif len(vArr) ==2:
            value = float(str(vArr[0]+"."+vArr[1]))

        unitstring = str(re.findall(r'[a-zA-Z]+',uiValue)[0])
        return self.getRawValue(value,unitstring)





