from BaseComponentClass import BaseComponentClass
from copy import deepcopy
from Utils.logger import *
from time import *
from selenium.webdriver import ActionChains
from Utils.utility import *
from Utils.UnitSystem import *
from Utils.Constants import *

import random
class TableComponentClass(BaseComponentClass):
    def __init__(self):
        BaseComponentClass.__init__(self)
        self.utility = __import__("Utils.utility")
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

    def getIterfaceHeaders(self,h):
        if h['HEADERROW'] != "":
            elHandle=h['HEADERROW']
            self.colCount = len(elHandle)
            return [str(eachHandler.text).strip() for eachHandler in elHandle]
        else:
            logger.debug("header is not present in table")

    def getIterfaceRows(self,colcount,h,length,selected=False):

        elHandle=h['ROWS']

        if len(elHandle) <1:
            logger.info("No DATA On Table")
            return Constants.NODATA


        rowCount = len(elHandle) / colcount
        if rowCount < length:
            l = len(elHandle)
        else:
            l = length*colcount
        rows = []
        temp = []
        #selected_rows=[]

        for i in range(0,l,colcount):
            j=i
            if not selected:
                rows.append([str(elHandle[j].text).strip() for j in range(j, j + colcount)])
                continue
            try:
                propertycolor=self.runtimeValue('bgcolor', elHandle[j].find_elements_by_xpath('../../..')[0])
                if self.rgb_to_hex(propertycolor) == Constants.TableSecltedColor and selected:
                    rows.append([str(elHandle[j].text).strip() for j in range(j, j + colcount)])
            except:
                logger.debug("Check manually Selected Rows= %d", j/colcount)
                pass

        return rows



    def scrollUpTable(self,h,driver):
        driver.d.execute_script("return arguments[0].scrollIntoView();", h['table']['ROWS'][0])
        sleep(4)
        while True:
            handle = self.utility.utility.getHandle(driver, "TableDummy_Screen", "table")
            if str(h['table']['ROWS'][0].text)==str(handle['table']['ROWS'][0].text):
                return
            else:
                import copy
                h=copy.deepcopy(handle)
                driver.d.execute_script("return arguments[0].scrollIntoView();", h['table']['ROWS'][0])
                # handle = self.utility.utility.getHandle(driver, "TableDummy_Screen", "table")["table"]




    def getRows1(self,colcount,h,length,driver,colIndex=0,scroll=False,ForTableData=False):

        if scroll:
            if len(h['ROWS']) > 7:
                driver.d.execute_script("return arguments[0].scrollIntoView();", h['ROWS'][len(h['ROWS'])-6*colcount])
            else:
                driver.d.execute_script("return arguments[0].scrollIntoView();", h['ROWS'][len(h['ROWS']) - 1 * colcount])

            sleep(4)
            h = self.utility.utility.getHandle(driver,"TableDummy_Screen","table")["table"]




        elHandle=h['ROWS']

        if len(elHandle)<1:
            logger.info("No DATA On Table")
            return Constants.NODATA



        rowCount = len(elHandle) / colcount
        rows = []
        temp = []

        for i in range(0,len(elHandle),colcount):
            j=i
            temp = [str(elHandle[j].text).strip() for j in range(j,j+colcount)]
            if any(temp):
                rows.append(temp)

        data = {}
        for row in rows:
            if colIndex == -1:
                data[str(row)] = row
            else:
                if row[colIndex] in data.keys():
                     row[colIndex]=row[colIndex]+"_DST"
                data[row[colIndex]] = row

        if ForTableData:
            return [rows,h]
        return [data, h]
        return rows

    def addrows(self,colcount,h,driver,length,colIndex):
        rows = {}
        while True:
            flag = True
            if not rows:
                t = self.getRows1(colcount,h,length,driver,colIndex)
                if t==Constants.NODATA:
                    return t
                rows = t[0]
                h = t[1]
                flag=False
            else:
                flag=True
                t = self.getRows1(colcount,h,length,driver,colIndex,True)
                newrows = t[0]
                h = t[1]

                for k in newrows.keys():
                    if k not in rows.keys():
                        flag = False
                        rows[k] = newrows[k]
            if flag:
                return rows



    def addrowsFormTableData(self,colcount,h,driver,length,colIndex,ForTableData=True):
        rowsList = []
        while True:
            flag = True
            if not rowsList:
                t = self.getRows1(colcount,h,length,driver,colIndex,ForTableData=ForTableData)
                if t==Constants.NODATA:
                    return t
                rowsList = t[0]
                h = t[1]
                flag=False
            else:
                flag=True
                t = self.getRows1(colcount,h,length,driver,colIndex,True,ForTableData=ForTableData)
                newrowsList = t[0]
                h = t[1]

                for newrow in newrowsList:
                    if newrow not in rowsList:
                        flag = False
                        rowsList.append(newrow)
            if flag:
                return rowsList








    def getAllRowsAfterScroll(self,colcount,h,parent,driver,length,colIndex):
        return self.addrows(colcount,h[parent],driver,length,colIndex)

    def getAllRowsAfterScrollForTableData(self, colcount, h, parent, driver, length, colIndex):
        return self.addrowsFormTableData(colcount, h[parent], driver, length, colIndex)



        # if rowCount <= 15:
        #     looprange=rowCount*colcount
        # else:
        #     looprange = 15 * colcount
        # for i in range(looprange):
        #     if len(temp) < colcount:
        #         temp.append(elHandle[i].text)
        #     else:
        #         rows.append(temp)
        #         temp = [elHandle[i].text]

        # return a 2D array

    def getRowIndexFromTable(self,columnIndex,tableHandle,value):
        data2=self.getTableData1(tableHandle,length=24)
        for index in range(len(data2['rows'])):
            if str(data2['rows'][index][columnIndex]).strip()==str(value):
                return index

        logger.info("row with column value  = %s not found in table",value)
        resultlogger.info("row with column value  = %s not found in table",value)
        return -1

    def getRowIndexFromTableWithScroll(self,setup,columnIndex,tableHandle,value):
        data2=self.getTableDataWithScroll(tableHandle,driver=setup)
        for index in range(len(data2['rows'])):
            if str(data2['rows'][index][columnIndex]).strip()==str(value):
                return index

        logger.info("row with column value  = %s not found in table",value)
        resultlogger.info("row with column value  = %s not found in table",value)
        return -1


    def getColumnValueFromTable(self,columnIndex,tableHandle):
        columnValue=[]
        data2=self.getTableData1(tableHandle)
        for index in range(len(data2['rows'])):
            columnValue.append(str(data2['rows'][index][columnIndex]).strip())
        return columnValue


    def getIterfaceTableData(self,h):
        handlers = self.compHandlers('table', h)
        data = {}
        data['header'] = self.getIterfaceHeaders(handlers)
        data['rows'] = self.getIterfaceRows(len(data['header']),handlers,15)
        return data


    def getSelection(self,handle,parent="table"):
        handlers = self.compHandlers(parent, handle)
        data={}
        return [[el.get_attribute('row'),el.text] for el in handlers['row-selection'] if el.text != ""]
        # data['selIndes']=handlers['row-selection'][len(handlers['row-selection']) - 1].get_attribute('row')
        # data['text']=handlers['row-selection'][len(handlers['row-selection']) - 1].text
        # return data


    def setSelection(self,index,h):
        handle = self.compHandlers('table', h)
        header = self.getIterfaceHeaders(handle)
        colCount=len(header)
        rand = random.randrange(colCount*index,colCount*index+4)
        handle['ROWS'][rand].click()

    def sortedInterfaceColum(self,index,handle):
        handlers = self.compHandlers('table', handle)
        handlers['CHECKSORT'][len(handlers['CHECKSORT'])-index].click()


    def getTableDataMap(self, h, parent="table", driver="", colIndex=0,length=15, child=""):
        # handlers = self.compHandlers('table', h)
        try:
            data = {}
            data['header'] = self.getIterfaceHeaders(h[parent])
            data['rows'] = self.getAllRowsAfterScroll(len(data['header']),h,parent,driver,length,colIndex)
            # data['rows'] = self.getIterfaceRows(len(data['header']),h[parent],length,driver)
            return data
        except Exception as e:
            return e




    def getTableDataWithScroll(self, h, parent="table", driver="", colIndex=0,length=15, child=""):
        try:
            data = {}
            data['header'] = self.getIterfaceHeaders(h[parent])
            data['rows'] = self.getAllRowsAfterScrollForTableData(len(data['header']),h,parent,driver,length,colIndex)
            # data['rows'] = self.getIterfaceRows(len(data['header']),h[parent],length,driver)
            return data
        except Exception as e:
            return e


    def setSelectionIndex(self,index,colCount,rowCount,h,driver=""):
        elHandle=h['ROWS']
        newIndex = (colCount)*(index-1)+1

        for i in range(len(elHandle)):
            if i == newIndex:
                if driver != "":
                    driver.execute_script("return arguments[0].scrollIntoView();", elHandle[i])
                elHandle[i].click()
                return True

    def getSelectedRow(self,h,parent='table',child='SELECTED_ROWS'):
        try:
            data = {}
            data['header'] = self.getIterfaceHeaders(h[parent])
            data['rows'] = self.getRows(h,parent,child)
            return data
        except Exception as e:
            return e

    def getRows(self,h,parent='table',child='SELECTED_ROWS'):
        elHandle=h[parent][child]

        if len(elHandle) <1:
            logger.info("No Row Selected on Table")
            return []

        rowCount = len(elHandle)
        rows = []

        for i in range(rowCount):
            rowValue=[]
            try:
                cellHandle=elHandle[i].find_elements_by_xpath('./div')
                for cell in cellHandle:
                    rowValue.append(str(cell.text).strip())
                rows.append(rowValue)
            except:
                logger.debug("Check manually Selected Rows= %d", i)
                pass

        return rows







    def scrollVertical(self):
        pass

    def getTableMap(self,h,parent="table",length=15,child="",columnName="Id"):
        return self.convertDataToDict(self.getTableData1(h),columnName)

    def getTableData1(self,h,parent="table",length=15,child="",selected=False):
        # handlers = self.compHandlers('table', h)
        try:
            data = {}
            data['header'] = self.getIterfaceHeaders(h[parent])
            data['rows'] = self.getIterfaceRows(len(data['header']),h[parent],length,selected)
            return data
        except Exception as e:
            return e

    # def setSelectionIndex(self,index,colCount,rowCount,h):
    #     elHandle=h['ROWS']
    #     newIndex = (colCount)*(index-1)+1
    #
    #     for i in range(len(elHandle)):
    #         if i == newIndex:
    #             elHandle[i].click()
    #             return True

    def setSelection1(self,index,h,parent,child=None):
        data = self.getTableData1(h,parent)
        colCount = len(data['header'])
        rowCount = len(data['rows'])
        return self.setSelectionIndex(index,colCount,rowCount,h[parent])

    def getDynamicText(self,h,parent,child=None):
        return h[parent]['count'][0].text

    def setSpecialSelection(self,driver,indices,key,h,parent="table",child=""):
        data = self.getTableData1(h,parent)
        colCount = len(data['header'])
        rowCount = len(data['rows'])
        self.setSelectionIndex(indices[0],colCount,rowCount,h[parent],driver)
        if len(indices) == 2:
            ActionChains(driver).key_down(key).perform()
            self.setSelectionIndex(indices[1],colCount,rowCount,h[parent],driver)
            ActionChains(driver).key_up(key).perform()


    def getTableCells(self,h,parent="table",child=None):
        handler = h[parent]['ROWS']
        cells = []

        for el in handler:
            cells.append(el.text)
        return cells



    def selectTableCell(self,value,h,parent="table",child=None):
        handler = h[parent]['ROWS']
        for el in handler:
            if el.text == value:
                try:
                    el.click()
                    return True
                except Exception as e:
                    return e

    def selectTableCellIndex(self,value,h,parent="table",child=None):
        handler = h[parent]['ROWS']
        for i in range(len(handler)):
            if i == value:
                try:
                    handler[i].click()
                    return handler[i].text
                except Exception as e:
                    return e

    def sortTable1(self,h,columnName,sortOrder="ASC",parent="table",child=""):
        try:
            headersHandle=h[parent]['HEADERROW']
            for el in headersHandle:
                if el.text.strip() == columnName:
                    logger.debug("Will Do Sort on Table Column %s",columnName)
                    try:
                        el.click()
                        logger.info("Sorted Table Column %s",columnName)
                        return True
                    except Exception as e:
                        logger.error("Exception %e found while sorting table on column %s",e,columnName)
                        return e
            logger.debug("Column Name %s not found on Table",columnName)
            return False
        except Exception as e:
            logger.error("Exception found while getting handle for header row : %s",e)


    # def sortTableAndValidateDate(self,h,columnName,sortOrder="ASC",parent="table",child=""):
    #     d = self.getTableData1(h)
    #     tableData = self.convertDataToDict(d)
    #     isSorted = self.sortTable1(h,columnName)
    #     sdata = self.getTableData1(h)
    #     stableData = self.convertDataToDict(sdata)


    def convertDataToDict(self,d,key="Id"):
        columnIndex = self.getIndexForValueInArray(d['header'],key)
        data={}
        for row in d['rows']:
            data[row[columnIndex]] = row
        return data

    def convertDataToDictWithKeyAsRow(self, d):
        #columnIndex = self.getIndexForValueInArray(d['header'], key)
        data = {}
        for row in d['rows']:
            data[str(row)] = row
        return data

    def getIndexForValueInArray(self,arr,value):
        for i in range(len(arr)):
            if str(value) == str(arr[i]).strip():
                return i
        return -1


    def getIndexForValueInArray1(self,arr,value):
        for i in range(len(arr)):
            if str(value) in str(arr[i]).strip():
                return i
        return -1

    def getColumnValueMap(self,d,index,columnName="Id"):
        columnIndex = self.getIndexForValueInArray(d['header'],columnName)
        temp = {}
        temp[str(d['rows'][index][columnIndex])] = d['rows'][index]
        return temp

    def getValueFromTable(self,list, iscount):
        l = []
        for i in range(len(list)):
            l.append(UnitSystem().getRawValueFromUI(str(list[i])))
        if iscount=='sum':
            return(str(sum(l)))
        elif iscount=='avg':
             return str(sum(l) / float(len(l)))
        else:
            return " "
            # if iscount=="sum":
            #   return value
