from classes.Components.DropdownComponentClass import *

def setFilter(setup,index=0,h="",parent="bulk_filter",child="list",occurence=0):
    commonElement = DropdownComponentClass()
    h1={}
    h1[parent]={}
    h1[parent][child]= h[parent][child][occurence].find_elements_by_css_selector("input[type=radio]")
    filtr={}
    filtr[str(h[parent][child][occurence].text).split("\n")[0]] = [str(commonElement.selectRadioButtonByIndex(index,h1,childDiv="label",parent=parent,child=child))]
    return filtr

def setCounters(setup,indices=[0],h="",parent="bulk_filter",child="list",occurence=0,clear=True):
    commonElement = DropdownComponentClass()
    h1={}
    if clear:
        logger.info("Clearing All Counter Selections by clicking 'none'")
        h[parent][child][occurence].find_elements_by_css_selector("u")[1].click()

    h1[parent]={}
    h1[parent][child]= h[parent][child][occurence].find_elements_by_css_selector("label.labelStyle")
    filtr={}
    filtr[str(h[parent][child][occurence].text).split("\n")[0]] = []

    for indx in indices:
        h1[parent][child][indx].click()
        if str(h1[parent][child][indx].find_elements_by_xpath("../div/input")[0].get_attribute("ng-reflect-checked")).lower() == "true":
            filtr[str(h[parent][child][occurence].text).split("\n")[0]].append(str(h1[parent][child][indx].text))
    return filtr


def getDataListContainer(setup,h="",parent="bulk_filter",child="list",occurence=0,comp="radio"):
    h1={}
    h1[parent]={}
    commonElement = DropdownComponentClass()
    if comp=="radio":
        h1[parent][child]= h[parent][child][occurence].find_elements_by_css_selector("input[type=radio]")
        return commonElement.getAllRadiosText(h1,childDiv="label",parent=parent,child=child)
    if comp=="a":
        h1[parent][child]= h[parent][child][occurence].find_elements_by_css_selector("a")
        return [ele.text for ele in  len(h1[parent][child])]
    if comp=="checkbox":
        h1[parent][child]= h[parent][child][occurence].find_elements_by_css_selector("label.labelStyle")
        return [ele.text for ele in  len(h1[parent][child])]


def setFormula(setup,h,source_parent="alllinks",source_child="a",target_parent="alltextareas",target_child="textarea",formulaId='0'):
    commonElement = DropdownComponentClass()
    formulae = setup.cM.getNodeElements("kpiformulae","formula")
    runtime_formula = ""
    for e in formulae[formulaId]['value']:
        if e == 'x':
            runtime_formula = runtime_formula + commonElement.clickLinkRandom(setup,h)
        else:
            commonElement.sendkeys_input(e,h,0,parent=target_parent,child=target_child,clear=False)
            runtime_formula = runtime_formula + e

    actual_formulaText = commonElement.getValue_input(h,0,parent=target_parent,child=target_child)

    import Utils.utility as util
    util.checkEqualAssert(runtime_formula,actual_formulaText,message="Verifying the Formula Value at Pop up only")

    return actual_formulaText

def convertChildstoKey(childs):
    d={}
    for child in childs:
        d[str(str(child.text.split("\n")[0])).strip()] = str(child.text.split("\n")[1])
    return d

def convertParentstoKey(parents):
    d={}
    for parent in parents:
        # d[str(parent.text.split("\n")[0])] = str(parent.text.split("\n")[2])
        d['total'] = str(parent.text.split("\n")[2])
        d['formula'] = str(parent.text.split("\n")[1]).replace(" ","")
    return d

def calculateValue(selectedParent,childs):
    # original_formula = formula
    commonElement = DropdownComponentClass()
    idMap = commonElement.merge_dictionaries(convertChildstoKey(childs),convertParentstoKey(selectedParent))
    original_formula = idMap['formula']
    import re
    arguments = re.split("\+|\-|\*|%|\/|\(|\)",idMap['formula'])
    formula=idMap['formula']
    for ele  in arguments:
        formula = str(formula).replace(str(ele),str(idMap[ele]))
    import Utils.utility as util
    calculatedvalue = eval(formula)
    util.checkEqualAssert(idMap['total'],str(calculatedvalue))
    return calculatedvalue

    # idMap[arguments]

# def checksum(total,)










