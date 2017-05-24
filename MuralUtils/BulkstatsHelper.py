from classes.Components.DropdownComponentClass import *
from Utils.utility import *
from MuralConstants import *
from classes.Pages.TrendingMonitoringPageClass import *

def setFilter(setup,index=0,h="",parent="bulk_filter",child="list",occurence=0):
    try:
        commonElement = DropdownComponentClass()
        h1={}
        h1[parent]={}
        h1[parent][child]= h[parent][child][occurence].find_elements_by_css_selector("input[type=radio]")
        filtr={}
        filtr[str(h[parent][child][occurence].text.split("\n")[0])] = [str(commonElement.selectRadioButtonByIndex(index,h1,childDiv="label",parent=parent,child=child))]
        return filtr
    except Exception as e:
        return e

def setCounters(setup,indices=[0],h="",parent="bulk_filter",child="list",occurence=0,clear=True):
    commonElement = DropdownComponentClass()
    h1={}
    if clear:
        logger.info("Clearing All Counter Selections by clicking 'none'")
        h[parent][child][occurence].find_elements_by_css_selector("u")[1].click()

    h1[parent]={}
    h1[parent][child]= h[parent][child][occurence].find_elements_by_css_selector("label.labelStyle")
    filtr={}
    filtr[str(h[parent][child][occurence].text.split("\n")[0])] = []

    for indx in indices:
        h1[parent][child][indx].click()
        if str(h1[parent][child][indx].find_elements_by_xpath("../div/input")[0].get_attribute("ng-reflect-checked")).lower() == "true":
            filtr[str(h[parent][child][occurence].text.split("\n")[0])].append(str(h1[parent][child][indx].text))
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


def setFormula(setup,h,source_parent="alllinks",source_child="a",target_parent="alltextareas",target_child="textarea",formulaId='0',force_clear=False):
    commonElement = DropdownComponentClass()
    formulae = setup.cM.getNodeElements("kpiformulae","formula")
    runtime_formula = ""
    if force_clear:
        commonElement.clear_input(h,parent=target_parent,child=target_child)

    for e in formulae[formulaId]['value']:
        if e == 'x':
            runtime_formula = runtime_formula + commonElement.clickLinkRandom(setup,h)
        else:
            commonElement.sendkeys_input(e,h,0,parent=target_parent,child=target_child,clear=False)
            runtime_formula = runtime_formula + e

    actual_formulaText = commonElement.getValue_input(h,0,parent=target_parent,child=target_child)

    import Utils.utility as util
    util.checkEqualAssert(runtime_formula.replace(" ",""),actual_formulaText.replace(" ",""),message="Verifying the Formula Value at Pop up only")

    return actual_formulaText

def getFormula(setup,h,source_parent="alllinks",source_child="a",target_parent="alltextareas",target_child="textarea"):
    commonElement = DropdownComponentClass()
    actual_formulaText = commonElement.getValue_input(h,0,parent=target_parent,child=target_child)
    return str(actual_formulaText)


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



def checkTextAfterDrag(drags,drop,key1="drag",key2="drop",k=0,setup=""):
    drag_drop = BaseComponentClass()
    drop_id_1 = key2+str(random.randint(0,100))

    for i in range(len(drags)):
        drag_id_1 = key1+str(i)
        text_drag_id_1 = drags[i].text

        drag_drop.set_attribute(setup,drags[i],"id",drag_id_1)
        drag_drop.set_attribute(setup,drop,"id",drop_id_1)
        logger.info("Going to perform Drag and Drop")
        drag_drop.dragDrop(setup,drag_id_1,drop_id_1)
        text_drop_id_1 = drop.text

        checkEqualAssert(True,text_drag_id_1.split("\n")[0].strip() in text_drop_id_1,message="Checking text at drag and drop, after drag-drop" + "Drag  = "+
                                                                       text_drag_id_1+ "Drop = "+text_drop_id_1)
        if k ==0:
            drags = getHandle(setup,"bulkstats_Screen","leftListContainer")['leftListContainer']['draggables']
            drop = getHandle(setup,"bulkstats_Screen","compareContainer")['compareContainer']['drop'][k]
            TMScreenInstance = TrendingMonitoringPageClass(setup.d)
            paths = TMScreenInstance.quicktrends.getPaths(getHandle(setup,MuralConstants.BULKSCREEN,"compareContainer"),
                                                          parent="compareContainer")
            checkEqualAssert(['#00CC99'],paths,message="Checking color and number of Lines")
        else:
            drags = getHandle(setup,"bulkstats_Screen","rightListContainer")['rightListContainer']['draggables']
            drop = getHandle(setup,"bulkstats_Screen","compareContainer")['compareContainer']['drop'][k]
            TMScreenInstance = TrendingMonitoringPageClass(setup.d)
            paths = TMScreenInstance.quicktrends.getPaths(getHandle(setup,MuralConstants.BULKSCREEN,"compareContainer"),
                                                          parent="compareContainer")
            checkEqualAssert(['#00CC99', '#990099'],paths,message="Checking color and number of Lines")


def checkSeverity(setup,input,selectedRowHandle):
    value = selectedRowHandle.text.split("\n")[2]
    commonelement = BaseComponentClass()

    if float(value) >= float(input['lthreshold']) and float(value) <= float(input['uthreshold']):
        color = commonelement.rgb_to_hex("rgb(51, 153, 102)")
    elif float(value) < float(input['lthreshold']):
        color = commonelement.rgb_to_hex("rgb(249, 245, 23)")
    elif float(value) > float(input['uthreshold']):
        color = commonelement.rgb_to_hex("rgb(240, 49, 23)")
    handle = getHandle(setup,MuralConstants.KPISCREEN)

    actual_color = commonelement.rgb_to_hex(handle['leftListContainer']['circle'][0].value_of_css_property(MuralConstants.BACKGROUNDCOLOR))

    checkEqualAssert(color,actual_color,message="Checking created KPI Rule for Severity as per formula")

# rgb(51, 153, 102)


    # idMap[arguments]

# def checksum(total,)










