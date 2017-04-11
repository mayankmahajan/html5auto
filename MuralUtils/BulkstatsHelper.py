from classes.Components.DropdownComponentClass import *

def setFilter(setup,index=0,h="",parent="bulk_filter",child="list",occurence=0):
    commonElement = DropdownComponentClass()
    h1={}
    h1[parent]={}
    h1[parent][child]= h[parent][child][occurence].find_elements_by_css_selector("input[type=radio]")
    filter={}
    filter[str(h[parent][child][occurence]).split("\n")[0]] = commonElement.selectRadioButtonByIndex(index,h1,childDiv="label",parent=parent,child=child)
    # return commonElement.selectRadioButtonByIndex(index,h1,childDiv="label",parent=parent,child=child)

