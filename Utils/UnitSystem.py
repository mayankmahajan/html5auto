import math
class UnitSystem :
    def __init__(self):
        pass
    metricUnits = ["", "K", "M", "B", "T", "P", "E", "Z", "Y"]
    metricValues = [1,1000,1000,1000,1000, 1000, 1000, 1000, 1000]
    byteUnits = ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]
    byteValues = [1,1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024]

    def getRawValue(self,convertedValue,unitString):
        if "bps" in unitString:
            unit = unitString.strip('bps')
            rawValue = convertedValue*self.byteValues[self.byteUnits.index(unit)]*math.pow(10,self.byteUnits.index(unit))
        else:
            rawValue = convertedValue*self.metricValues[self.metricUnits.index(unitString)]*math.pow(10,self.byteUnits.index(unitString))
        return rawValue




