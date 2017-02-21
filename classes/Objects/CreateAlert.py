import random
from Utils.ConfigManager import *
from MuralUtils.MuralConstants import *
from classes.Objects.Time import *

class CreateAlert:
    def __init__(self,ruleName="automationrule",measure={},type=0,gran=0,conditions=[],time=[],filters=0,status="Active"):

        c = ConfigManager()
        maxFilters  = 5
        maxConditonValue = 1000

        t = c.getAllNodeElements("measuretypes","type")
        g = ["Hourly","Daily","Monthly"]
        operator = ["=",">","<"]
        type=random.randint(0,len(t)-1)
        gran=random.randint(0,len(g)-1)
        totalFilters=random.randint(1,maxFilters)

        # print(type,gran,totalFilters)

        u=c.getNodeElements("unitsystem","unit")
        m= c.getNodeElements("measures","measure")
        measuretypes = c.mergeTwoNodes(m,u,"unitSystem")
        measures = c.getAllNodeElements("measures","measure")

        # t = ["absolute","rateofchange"]
        # t = c.getAllNodeElements("measuretypes","type")
        # g = ["Hourly","Daily","Weekly"]


        self.ruleName = ruleName
        self.status = status
        self.measure = measuretypes[measures[random.randint(0,len(measures)-1)]]
        unitValues = self.measure['unitvalues'].split(',')

        self.type = t[type]
        self.gran = g[gran]
        self.conditions = [self.createCond(operator, maxConditonValue, unitValues,self.type), self.createCond(operator, maxConditonValue, unitValues,self.type), self.createCond(operator, maxConditonValue, unitValues,self.type)]

        self.filters =[]
        for i in range(0,totalFilters):
            self.filters.append([1,1])

        availableTime = c.getNodeElements("availabletimerange","time")
        st = availableTime[MuralConstants.STARTTIME]
        et = availableTime[MuralConstants.ENDTIME]

        self.time = [Time(st['year'],st['month'],st['day'],st['hour'],st['min']),Time(et['year'],et['month'],et['day'],et['hour'],et['min'])]

        self.dict = {}
        self.dict['time'] =self.time
        self.dict['conditions'] = self.conditions
        self.dict['type'] = self.type
        self.dict['gran'] = self.gran
        self.dict['filters'] = self.filters
        self.dict['measure'] = self.measure
        self.dict['ruleName'] = self.ruleName
        self.dict['status'] = self.status

        # self.filters = filters
        # return self

    def createCond(self, operator, maxnumber, unitValues,type):
        if 'rate' in str(type).lower():
            return str(operator[random.randint(0,len(operator)-1)])+str(random.randint(0,maxnumber))
        else:
            return str(operator[random.randint(0,len(operator)-1)])+str(random.randint(0,maxnumber))+str(unitValues[random.randint(0,len(unitValues)-1)])


# x =CreateAlert()


