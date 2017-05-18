# from classes.DriverHelpers.DriverHelper import DriverHelper
# from selenium import webdriver
# webdriver.Firefox().find_element_by_xpath().send_keys()
from Utils.UnitSystem import UnitSystem
from Utils.ConfigManager import ConfigManager
from selenium.common.exceptions import *
import time
from Utils.logger import *
from Utils.resultlogger import *
from selenium.webdriver.common.keys import *
from Utils.Constants import *

class BaseComponentClass:
    def __init__(self):
        self.utility = __import__("Utils.utility")
        self.colors = self.configmanager.getNodeElements("colors","color")
        self.unitsystem = UnitSystem()

    def click(self, elHandle):

        try:
            elHandle.click()
            return True
        except Exception:
            return Exception


    def send_keys(self, elHandle, value):
        return elHandle.send_keys(value)

    def totalvalueformlist(self,list,flag="sum",unitValue=1024.0):
            unitstring=""
            import re
            for list_value in list:
                if len(re.findall(r'[a-zA-Z]+',str(list_value)))!=0:
                    unitstring = str(re.findall(r'[a-zA-Z]+',str(list_value))[0])
                    break

            l = []
            for i in range(len(list)):
                l.append(UnitSystem().getRawValueFromUI(str(list[i])))
            if flag == 'sum':
                return UnitSystem().getValueFromRawValue(sum(l),unitValue,unitstring=unitstring)
            elif flag == 'avg':
                return UnitSystem().getValueFromRawValue(sum(l)/float(len(l)),unitValue,unitstring=unitstring)
            else:
                return " "


    def customClick(self, elHandle):
        try:
            logger.info("Going to perform Custom Click")
            elHandle[len(elHandle)-1].click()
            time.sleep(2)
            return True
        except TypeError or IndexError or Exception as e:
            elHandle.click()
            return e
        # return elHandle[len(elHandle)-1].click()
    def customSendkeys(self, elHandle, value):
        return elHandle[len(elHandle)-1].send_keys(value)
    def customText(self,elHandle):
        return elHandle[len(elHandle)-1].text


    def text(self,elHandle):
        return elHandle.text

    def getSelection(self):
        '''
        Base method for getSelection that can be used across all components for uniformity
        :return: Selection
        '''
        selection = []
        return selection

    def getSpecificLocators(self,locatorClass):
        '''
        Can be overridden at ComponentClass
        :param locatorClass: Locator Class of Component
        :return: component child as Key and its locators as Value
        '''
        return self.dictionary_ele_locators(locatorClass)

    def dictionary_ele_locators(self, locatorClass):
        dic = {}
        for method in dir(locatorClass):
            if type(getattr(locatorClass,method)) == tuple:
                dic[method]= getattr(locatorClass,method)
        return dic

    def validateToolTipData(self,dataCollection):
        result = {}
        return result

    def compare(self,v1,v2):
        if v1 == v2:
            return True
        else:
            return False

    def __init__(self):
        self.unitSystem = UnitSystem()
        self.configmanager = ConfigManager()


    def compHandlers(self,comp,handlers):
        return handlers[comp]
        # newHandlers = {}
        # for k,v in handlers.iteritems():
        #     if k in self.configmanager.componentChildRelations[comp]:
        #         newHandlers[k] = v
        # return newHandlers


    def selectDropDownByText(self,handler,text,text2="HAHA"):
        for ele in handler.find_elements_by_xpath(".//*"):
            if ele.text == text or ele.text == text2:
                ele.click()
                return ele.text

    def doSelection(self,h,parentLocator,measure):
        handlers = self.compHandlers('measureselectors',h)
        measureArr=measure.split("_")
        measureName=measureArr[0]
        downUpTotal=measureArr[1]
        absPerc=measureArr[2]
        self.setMeasureName(measureName,handlers['primaryMeasure'])
        self.select(handlers[downUpTotal])
        self.select(handlers[absPerc])
        try:
            avgPeak=measureArr[3]
            self.select(handlers[avgPeak])
        except:
            print "Got Measure without Peak/Average %s",measureName

    def getAllActiveElements(self, childHandles):
        activeElements = []
        for ele in childHandles:
            # 'disabled' not in ele.get_attribute("class") and
            if ele.is_displayed():
                activeElements.append(ele)
            else:
                pass
        return activeElements

    def clickCheckBox(self,h,index,parent="allcheckboxes",child="checkbox"):
        try:
            logger.debug("Going to Click Checkbox %d parent %s and child %s ",index,parent,child)
            h[parent][child][index].click()
            return True
        except Exception as e:
            logger.error("Exception found while clicking Checkbox %d",index)
            return e

    # def isCheckBoxEnabled(self,h,index,parent="allcheckboxes",child="checkbox"):
    #     try:
    #         logger.debug("Going to get State of Checkbox %d parent %s and child %s ",index,parent,child)
    #         state = True if str(h[parent][child][index].get_attribute("ng-reflect-model")).lower() == 'true' else False
    #         logger.debug("Got State of Checkbox %d parent %s and child %s as %s",index,parent,child,str(state))
    #         return state
    #     except Exception as e:
    #         logger.error("Exception found while clicking Checkbox %d",index)
    #         return e

    def clickCheckBoxWithName_UMMural(self,h,value,parent="allcheckboxes",child="checkbox",UserRole='0',force=False):
        try:
            value_list=value.split(".")
            logger.debug("Going to Click Checkbox with Name %s parent %s and child %s ",value_list[len(value_list)-1], parent, child)
            info=self.getCheckBoxElementWithName_UMMural(h,str(value_list[len(value_list)-1]),UserRole=UserRole)
            if str(info[2])=='True':
                if str(info[1])=="1" and force==True:
                    h[parent][child][int(info[0])].click()
                    return self.getCheckBoxElementWithName_UMMural(h,str(value_list[len(value_list)-1]),UserRole=UserRole)

                elif str(info[1])=="1" and force==False:
                    return self.getCheckBoxElementWithName_UMMural(h,str(value_list[len(value_list)-1]),UserRole=UserRole)
                else:
                    h[parent][child][int(info[0])].click()
                    return self.getCheckBoxElementWithName_UMMural(h,str(value_list[len(value_list)-1]),UserRole=UserRole)
            else:
                for l in range(len(value_list)):
                    info=self.getCheckBoxElementWithName_UMMural(h,str(value_list[l]),UserRole=UserRole)
                    h[parent][child][int(info[0])].click()

                return self.getCheckBoxElementWithName_UMMural(h,str(value_list[len(value_list)-1]),UserRole=UserRole)

        except Exception as e:
            logger.error("Exception found while clicking Checkbox %s", value)
            return e




    def getAllCheckBoxElement_UMMural(self,h,parent="allcheckboxes",child="checkbox",UserRole="0"):
        try:
            data={}
            checkedlist=[]
            uncheckedlist=[]
            logger.debug("Going to find all active and inactive elements of checkbox")
            for i in range(len(h[parent][child])):
                value=str(h[parent][child][i].find_elements_by_xpath('..')[0].text)
                check_value=self.isCheckBoxSelected_UMMural(h,i)

                if check_value==0:
                    uncheckedlist.append(value)
                else:
                    checkedlist.append(value)

                check_state=self.isCheckBoxEnabled_UMMural(h,i,UserRole=UserRole)
                data[value]=[check_value,check_state]

            return data,checkedlist,uncheckedlist
        except Exception as e:
            logger.error("Exception found while getting elements of checkbox")


    def getCheckBoxElementWithName_UMMural(self,h,value,parent="allcheckboxes",child="checkbox",UserRole="0"):
        try:
            logger.debug("Going to find checkbox (state and value ) corresponding to %s",value)
            for i in range(len(h[parent][child])):
                if str(value)==str(h[parent][child][i].find_elements_by_xpath('..')[0].text):
                    check_value=self.isCheckBoxSelected_UMMural(h,i)
                    check_state=self.isCheckBoxEnabled_UMMural(h,i,UserRole=UserRole)
                    return [i,check_value,check_state]
            logger.error("%s not found in checkbox list",value)
            return[-1,0,False]

        except Exception as e:
            logger.error("Exception found while getting elemennts of checkbox")


    def isCheckBoxSelected_UMMural(self,h,index,parent="allcheckboxes",child="checkbox"):
        try:
            logger.debug("Going to get State of Checkbox %d parent %s and child %s ", index, parent, child)
            state=h[parent][child][index].is_selected()
            logger.debug("Got State of Checkbox %d parent %s and child %s as %s", index, parent, child, str(state))
            if state==True:
                return 1
            else:
                return 0
        except Exception as e:
            logger.error("Exception found while checking Checkbox %d", index)
            return e


    def isCheckBoxSelected_MRX(self,h,index,parent="allcheckboxes",child="checkbox"):
        try:
            logger.debug("Going to get State of Checkbox %d parent %s and child %s ", index, parent, child)

            propertycolor = self.runtimeValue('bgcolor', h[parent][child][index].find_elements_by_xpath('../../..')[0])
            state=self.rgb_to_hex(propertycolor) == Constants.TableSecltedColor
            logger.debug("Got State of Checkbox %d parent %s and child %s as %s", index, parent, child, str(state))
            if state==True:
                return 1
            else:
                return 0

        except Exception as e:
            logger.error("Exception found while checking Checkbox %d", index)
            return e




    def isCheckBoxSelectedWithName_UMMural(self,h,value,parent="allcheckboxes",child="checkbox"):
        try:
            logger.debug("Going to get State of Checkbox %s parent %s and child %s ", value, parent, child)
            for i in range(len(h[parent][child])):
                if str(value) == str(h[parent][child][i].find_elements_by_xpath('..')[0].text):
                    state = h[parent][child][i].is_selected()
                    logger.debug("Got State of Checkbox %s parent %s and child %s as %s", value, parent, child, str(state))
                    if state==True:
                       return 1
                    else:
                        return 0
            return -1
        except Exception as e:
            logger.error("Exception found while checking Checkbox %s", value)
            return e




    def isCheckBoxEnabledWithName_UMMural(self,h,value,parent="allcheckboxes",child="checkbox",UserRole="0"):
        try:
            logger.debug("Going to check whether Checkbox %s is enable or disable parent %s and child %s ", value, parent, child)
            for i in range(len(h[parent][child])):
                if str(value) == str(h[parent][child][i].find_elements_by_xpath('..')[0].text):
                    logger.debug("Got State of Checkbox %s parent %s and child %s ", value, parent, child)
                    if UserRole=="0":
                        if h[parent][child][i].is_enabled():
                            return True
                        else:
                            return False
                    elif UserRole=="1":
                        if len(h[parent][child][i].find_elements_by_xpath('../../../../div[@class="disableContainer"]')) != 0:
                            return False
                        else:
                            return True
        except Exception as e:
            logger.error("Exception found while checking Checkbox having value = %s Enable or Disable", value)
            return e

    def isCheckBoxEnabled_UMMural(self,h,index,parent="allcheckboxes",child="checkbox",UserRole="0"):
        try:
            logger.debug("Going to check whether Checkbox at index %d is enable or disable parent %s and child %s ", index, parent, child)
            if UserRole=="0":
                if h[parent][child][index].is_enabled():
                    return True
                else:
                        return False

            elif UserRole=="1":
                if len(h[parent][child][index].find_elements_by_xpath('../../../../div[@class="disableContainer"]')) != 0:
                    return False
                else:
                    return True
        except Exception as e:
            logger.error("Exception found while checking Checkbox having value = %s Enable or Disable", str(e))
            return e


    def isCheckBoxEnabled(self,h,index,parent="allcheckboxes",child="checkbox"):
        try:
            logger.debug("Going to get State of Checkbox %d parent %s and child %s ",index,parent,child)
            state = True if str(h[parent][child][index].find_element_by_xpath("../input").get_attribute("ng-reflect-checked")).lower() == 'true' else False

            # state = True if str(h[parent][child][index].get_attribute("ng-reflect-model")).lower() == 'true' else False
            logger.debug("Got State of Checkbox %d parent %s and child %s as %s",index,parent,child,str(state))
            return state
        except Exception as e:
            logger.error("Exception found while clicking Checkbox %d",index)
            return e

    def clear_input(self,h,parent="allinputs",child="input",index=0):
        h[parent][child][index].send_keys(len(str(h[parent][child][index].get_attribute("value")))*Keys.BACKSPACE)

    def sendkeys_input(self,value,h,index,parent="allinputs",child="input",clear=True):
        try:
            if clear:
                logger.debug("Clearing the text at input %d parent %s and child %s ",index,parent,child)
                # h[parent][child][index].send_keys(len(str(h[parent][child][index].get_attribute("value")))*Keys.BACKSPACE)
                self.clear_input(h,parent,child,index)
            logger.debug("Going to send keys to input %d parent %s and child %s ",index,parent,child)

            h[parent][child][index].send_keys(value)
            return self.getValue_input(h,index,parent,child)
            return h[parent][child][index].get_attribute("value")
        except Exception as e:
            logger.error("Exception found while entering keys to input %d",index)
            return e

    def getValue_input(self,h,index,parent="allinputs",child="input"):
        time.sleep(2)
        return h[parent][child][index].get_attribute("value")


    def clickSpanWithTitle(self,value,h,parent="allspans",child="span"):
        for el in h[parent][child]:
            logger.info("Searching span with title = %s",str(value))
            if str(value) == el.text:
                try:
                    logger.info("Got span with title = %s, now clicking it",str(value))
                    el.click()
                    return True
                except Exception as e:
                    logger.error("Exception found while clicking Span with Title = %s",str(value))
                    return e
        logger.debug("Span with title = %s not found",str(value))
        return False

    def selectRadioButton(self, value, h, childDiv="span", parent="radios", child="radio"):
        childs = ".//" + childDiv

        for el in h[parent][child]:
            if value == el.find_elements_by_xpath(childs)[0].text.strip().strip(':').strip():
                try:
                    el.click()
                    el.find_elements_by_xpath(".//input")[0].click()
                    time.sleep(2)
                    return True
                except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                    return e
        return False


    def getSelectedRadioButtonText(self,h,childDiv="input", parent="radios", child="radio"):
        for el in h[parent][child]:
            logger.info("Searching Selected Button")
            if el.find_elements_by_tag_name(childDiv)[0].is_selected():
                return el.text

        return False



    def getAllSiblings(self, h, text="Rule", tag="span", child="alertinfo"):
        tagpath = "..//"+tag
        for el in h[child][0].find_elements_by_tag_name(tag):
            if el.text == text:
                return el.find_elements_by_xpath(tagpath)


    def clickButton(self,value,h,parent="allbuttons",child="button"):
        for el in h[parent][child]:
            try:
                if value == el.text.strip() or str(value).lower() == str(el.text.strip()).lower():
                    try:
                        el.click()
                        time.sleep(2)
                        return True
                    except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                        return e
            except Exception as e:
                return e
        return False

    def clickImage(self,value,h,parent="allimages",child="image"):
        for el in h[parent][child]:
            try:
                if value in str(el.get_attribute("class")).strip():
                    try:
                        el.click()
                        time.sleep(2)
                        return True
                    except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                        return e
            except Exception as e:
                return e
        return False

    def isButtonEnabled(self,value,h,parent="allbuttons",child="button"):
        for el in h[parent][child]:
            try:
                if value == el.text.strip():
                    try:
                        return el.is_enabled()
                    except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                        return e
            except Exception as e:
                return e
        return False


    def clickInputButton(self,value,h,parent="allbuttons",child="ibutton"):
        for el in h[parent][child]:
            try:
                if value == el.get_attribute('value').strip():
                    try:
                        el.click()
                        time.sleep(2)
                        return True
                    except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                        return e
            except Exception as e:
                return e
        return False


    def runtimeValue(self,prop,ele):
        if prop == "text":
            return ele.text
        elif prop == "title":
            return ele.get_attribute("title")
        elif prop == "value":
            return ele.get_attribute("style")
        elif prop == "style":
            return ele.get_attribute("style")
        elif prop == "class":
            return ele.get_attribute("class")
        elif prop == "id":
            return ele.get_attribute("id")
        elif prop == "bgcolor":
            return ele.value_of_css_property("background-color")


    def validateData(self,dataCollection,csvData):
        result = {}
        # for key,value in csvData.iteritems():
        for key in dataCollection['btvData']['dimension']:
            if "All " in key or "Others" in key:
                pass
            else:
                UIData = 0.0
                convertedData = float(dataCollection['btvData']['value'][dataCollection['btvData']['dimension'].index(key)].split(" ")[0])
                unitString = dataCollection['btvData']['value'][dataCollection['btvData']['dimension'].index(key)].split(" ")[1]
                UIData = self.unitSystem.getRawValue(convertedData,unitString)

                if csvData[key]['AGGR_totalByteBuffer'] == UIData:
                    result[key] = "Data Validation PASSED"
                else:
                    result[key] = "Data Validation FAILED --> Actual : "+str(UIData)+" and Expected : "+str(csvData[key]['AGGR_totalByteBuffer'])

        return result

    def getFormattedFilters(self,arr,skipIndex=2):
        filters = {}
        for i in range(0,len(arr),skipIndex):
            filters[arr[i].strip().strip(':').strip()]=self.getCommaSeparatedValues(arr[i+1])
        return filters


    def getCommaSeparatedValues(self,string):
        return [e.strip() for e in str(string).strip().split(',')]

    def selectRadioButtonByIndex(self, index, h, childDiv="span", parent="radios", child="radio"):
        childs = ".//" + childDiv

        for i in range(len(h[parent][child])):
            if i == index:
                try:
                    h[parent][child][i].click()
                    try:
                        h[parent][child][i].find_elements_by_xpath(".//input")[0].click()
                    except:
                        pass

                    time.sleep(2)
                    try:
                        return h[parent][child][i].find_elements_by_xpath(childs)[0].text.strip().strip(':').strip()
                    except:
                        return h[parent][child][i].find_elements_by_xpath("."+childs)[0].text.strip().strip(':').strip()
                except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                    return e
        return False

    def getAllRadiosText(self, h, childDiv="span", parent="radios", child="radio"):
        return [self.getRadioButtonText(e,h,childDiv,parent,child) for e in len(h[parent][child])]

    def getRadioButtonText(self, index, h, childDiv="span", parent="radios", child="radio"):
        childs = ".//" + childDiv

        for i in range(len(h[parent][child])):
            if i == index:
                try:
                    try:
                        return h[parent][child][i].find_elements_by_xpath(childs)[0].text.strip().strip(':').strip()
                    except:
                        return h[parent][child][i].find_elements_by_xpath("."+childs)[0].text.strip().strip(':').strip()
                except ElementNotVisibleException or ElementNotSelectableException or Exception as e:
                    return e
        return False

    def rgb_to_hex(self,r):
        rgb = str(r)
        if '#' in rgb:
            return rgb
        elif 'rgba' not in rgb and 'rgb' in rgb:
            x = rgb.split('rgb')[1].strip('\(').strip('\)').split(',')
        elif 'rgb' not in rgb:
            x = rgb.strip('\(').strip('\)').split(',')
        else:
            # ignoring alpha property
            x= rgb.split('rgba')[1].strip('\(').strip('\)').split(',')

        rgb = (int(x[0]),int(x[1]),int(x[2]))
        return '#%02x%02x%02x' % rgb

    def takeScreenshot(self,driver):
        import random
        r = "issue_" + str(random.randint(0, 9999999)) + ".png"
        driver.save_screenshot(r)
        logger.error("UI is not present or loaded. Screenshot dumped with %s", str(r))
        resultlogger.info("******* UI is not present or loaded. Screenshot dumped with %s", str(r))


    def checkSpecificElement(self,setup,list):
        elementtobechecked = setup.cM.getNodeElements("specificrowsinbtv", "row")
        elements = []
        for key, row in elementtobechecked.iteritems():
            elements.append(row['locatorText'])

        for element in elements:
            if element in list:
                self.utility.utility.checkEqualAssert(False,element in list[:-2],"","","Verify location of %s in component"+element)
        return True



    @staticmethod
    def merge_dictionaries(d1,d2):
        n = d1.copy()
        n.update(d2)
        return n

    def calTotal(self,dimList,valueList,measureSelected,metricMeasure='Flows',metricMeasure1='Hits',timeMeasure='Avg'):
        data = {}
        if (metricMeasure in measureSelected or metricMeasure1 in measureSelected) and len(valueList)!=0:
            data['totalValue']=self.totalvalueformlist(valueList,unitValue=1000)
        elif timeMeasure in measureSelected and len(valueList)!=0:
            data['totalValue']=self.totalvalueformlist(valueList,flag="avg",unitValue=60)
        elif len(valueList)!=0:
            data['totalValue'] = self.totalvalueformlist(valueList)
        else:
            data['totalValue'] = ""

        data['dimSelected'] =""
        if len(dimList)!=0:
            for dim in dimList:
                if data['dimSelected']=="":
                    data['dimSelected']=str(dim)
                else:
                    data['dimSelected']=data['dimSelected']+", "+str(dim)

        return data

    def set_attribute(self,setup,elem,property,value):
        setAtr = 'arguments[0].setAttribute(arguments[1],arguments[2])'
        setup.d.execute_script(setAtr,elem,property,value)

    def dragDrop(self,setup,source,target):
        # selectedRows = setup.d.execute_script('return $(".selectedRowClass")')
        with open("/Users/mayank.mahajan/PycharmProjects/html5automation/classes/DriverHelpers/drag_and_drop_helper.js","r") as f:
            java_script = f.read()
            method = ".simulateDragDrop"
        src='$("#'+source+'")'
        trg = '({"dropTarget":"#'+target+'"});'
        setup.d.execute_script(java_script)
        time.sleep(8)
        print src+method+trg
        setup.d.execute_script(src+method+trg)

    def clickLink(self,value,handle,parent="alllinks",child="a"):
        for el in handle[parent][child]:
            if el.text == value:
                try:
                    logger.info("Going to click link %s",el.text)
                    el.click()
                    return True
                except ElementNotSelectableException or Exception as e:
                    logger.error("Exception found while clicking %s = %s",el.text,e)
                    return e
        logger.error("Link Text not found = %s",el.text)
        return False

    def clickLinkRandom(self,setup,handle,parent="alllinks",child="a"):
        import random
        try:
            if len(handle[parent][child]) <1:
                self.takeScreenshot(setup.d)
                logger.debug("No Link available to click")
                raise
            index = random.randint(0,len(handle[parent][child]))
            self.dispatchDoubleClick(setup,handle[parent][child][index])
            return str(handle[parent][child][index].text)
        except Exception as e:
            logger.error("Got Exception while clicking Random Links = %s",str(e))
            raise e

    def dispatchDoubleClick(self,setup,el):
        js = "var event = new MouseEvent('dblclick', {'view': window,'bubbles': true,'cancelable': true});"
        script = "arguments[0].dispatchEvent(event);"
        setup.d.execute_script(js+script,el)

    def getColorName(self,col):
        for color in self.colors:
            if col in color or str(col).lower() in color:
                return str(color).split('#')[0]
        return str(col)