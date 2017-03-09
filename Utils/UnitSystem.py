import math

class UnitSystem :
    def __init__(self):
        pass
    metricUnits = ["", "K", "M", "B", "T", "P", "E", "Z", "Y"]
    metricValues = [1,1000,1000,1000,1000, 1000, 1000, 1000, 1000]
    byteUnits = ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]
    byteValues = [1,1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024]
    timeUnits = ["s","m"]
    timeValues = [1,"60"]

    def getRawValue(self,convertedValue,unitString):
        convertedValue = float(convertedValue)
        if "bps" in unitString:
            unit = unitString.strip('bps')
            rawValue = convertedValue*self.byteValues[self.byteUnits.index(unit)]*math.pow(10,self.byteUnits.index(unit))
        else:
            rawValue = convertedValue*self.metricValues[self.metricUnits.index(unitString)]*math.pow(10,self.byteUnits.index(unitString))
        return rawValue

    def getRawValueFromUI(self,uiValue):
        import re
        vArr =  re.findall('[0-9]+',uiValue)
        if len(vArr) ==1 :
            value = float(vArr[0])
        elif len(vArr) ==2:
            value = float(str(vArr[0]+"."+vArr[1]))

        unitstring = str(re.findall(r'[a-zA-Z]+',uiValue)[0])
        return self.getRawValue(value,unitstring)





