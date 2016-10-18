from BaseComponentClass import BaseComponentClass
from copy import deepcopy
from Utils.logger import *
from time import *
class TableComponentClass(BaseComponentClass):
    colCount = 0
    rowCount = 0
    def doSingleSelection(self):
        BaseComponentClass.click()

    def getData(self,driver,h):
        '''
        Returns Data as Dictionary with Name and Value
        :param handlers: Handlers to all the components
        :return: Data from the Bar Chart
        '''
        data = {}
        handlers = self.compHandlers('table',h)
        #HardCoded for time being
        try:
            driver.execute_script("return arguments[0].scrollIntoView();", handlers['ROWS'][len(handlers['ROWS'])-1])
        except:
            pass

        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[key]["action"] == "getData":

                # This has to be unique for every component
                data[key] = self.getTableData(key,value)

        d = self.getDimensionMeasureDict(data)
        return d

    def getTableData(self, key, elHandle):
        '''
        This method is iterated for all the components with action getData
        :param elHandle: Handler to Column in Table
        :return: Data from Table
        '''
        d = {}
        t = [] # Total Row
        r = [] # Rows
        c1 = [] # Column 1

        if 'HEADER' in key.upper():
            self.colCount = len(elHandle)
            return [eachHandler.text for eachHandler in elHandle]
        else:
            self.rowCount = (len(elHandle) - self.colCount)/self.colCount
            tr = [] # Temp Row
            for i in range(0,len(elHandle)+1):
                if i < self.colCount:
                    t.append(elHandle[i].text)
                    continue
                elif i >= self.colCount and i < (self.colCount+self.rowCount):
                    c1.append(elHandle[i].text)
                    continue
                else:
                    if len(tr) == self.colCount-1:
                        r.append(tr)
                        tr = []
                    try:
                        tr.append(elHandle[i].text)
                    except:
                        pass


            d['FOOTERROW'] = t
            d['DATAROWS'] = r
            d['COLUMN1'] = c1
            return d



    def getDimensionMeasureDict(self,c):
        d =deepcopy(c['ROWS'])
        a = deepcopy(c)
        headerC1 = deepcopy(a['HEADERROW']).pop(0)
        measures = a['HEADERROW'][1:]
        data = {}
        totalKey = deepcopy(d['FOOTERROW']).pop(0)
        data[totalKey] = d['FOOTERROW'][1:]

        temp = {}
        for i in range(0,len(d['COLUMN1'])):
            temp[d['COLUMN1'][i]] = {}
            for j in range(0,self.colCount-1):
                temp[d['COLUMN1'][i]][measures[j]] = d['DATAROWS'][i][j]

        # for key in d['COLUMN1']:
        #     temp = {}
        #     for i in range(0,self.colCount-1):
        #         for j in range(0,self.rowCount):
        #             for k in range(1,self.colCount):
        #                 temp[measures[i]] = d['DATAROWS'][j][k]
        temp[totalKey] = {}
        for j in range(1,self.colCount-1):
            temp[totalKey][measures[j-1]] = d['FOOTERROW'][j]

        return temp

    def sortTable(self,driver,h,measure,order='ASC'):

        '''

        :param driver:
        :param h:
        :param measure:
        :param order:
        :return:
        '''

        handlers = self.compHandlers('table',h)
        #HardCoded for time being
        try:
            driver.execute_script("return arguments[0].scrollIntoView();", handlers['ROWS'][len(handlers['ROWS'])-1])
        except:
            pass

        for key,value in handlers.iteritems():
            if self.configmanager.componentSelectors[key]["action"] == "sort":

                # This has to be unique for every component
                # if 'HEADER' in key.upper():
                for eachHandler in handlers[key]:
                    if eachHandler.text == measure:
                        driver.execute_script("return arguments[0].scrollIntoView();", handlers['ROWS'][len(handlers['ROWS'])-self.colCount+1])
                        try:
                            eachHandler.click()
                            logger.info("Column with Measure : %s sorted ASC", measure)
                        except Exception as e:
                            logger.error("Exception Caught : %s", str(e))
                        return order

                        # logger.info("Column with Measure : %s sorted ASC", measure)
                        # time.sleep (5)
                        # if order == "ASC":
                        #     return order
                        # else:
                        #     eachHandler.click()
                        #     logger.info("Column with Measure : %s sorted DSC", eachHandler.text)
                        #     return order

    def getSortedColumn(self,driver,h):
        '''

        :param driver:
        :param h:
        :return:
        '''
        handlers = self.compHandlers('table',h)
        try:
            driver.execute_script("return arguments[0].scrollIntoView();", handlers['ROWS'][len(handlers['ROWS'])-1])
        except:
            pass




















