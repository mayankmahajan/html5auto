import math
import xml.etree.ElementTree as ET
import glob
from Utils.ConfigManager import ConfigManager
#
# def is_prime(number):
#     if number > 1:
#         if number == 2:
#             return True
#         if number % 2 == 0:
#             return False
#         for current in range(3, int(math.sqrt(number) + 1), 2):
#             if number % current == 0:
#                 return False
#         return True
#     return False

import json
from pprint import pprint


def run():
    # xml_files = glob.glob("*.xml")
    xml_files = ["/Users/mayank.mahajan/Downloads/acumeMemStorage"]

    xml_element_tree = None
    for xml_file in xml_files:
        data = ET.parse(xml_file).getroot()
        # print ElementTree.tostring(data)
        for result in data.iter('tbody'):
            if xml_element_tree is None:
                xml_element_tree = data
                insertion_point = xml_element_tree.findall("./tbody")[0]
            else:
                insertion_point.extend(result)
    if xml_element_tree is not None:
        sConfigs = xml_element_tree.findall("./tbody")
        print ET.tostring(xml_element_tree)






if __name__ == '__main__':
    # run()
    configmanager = ConfigManager()
    # x = configmanager.getScreenConfigs()
    # y = configmanager.getComponentConfigs()
    # z = configmanager.getSelectionParams()
    # a =configmanager.getComponentChildRelations()
    b= configmanager.getComponentSelectors()



    # solTree = ET.parse('../configs/solutionconfig.xml')
    # coreTree = ET.parse('../configs/coreconfig.xml')


    # import xml.etree.ElementTree as ET
    #
    # tree = ET.parse('../configs/solutionconfig.xml')
    # root = tree.getroot()
    # print root
    # with open('../configs/solutionconfig.json') as data_file:
    #     data = json.load(data_file)
    # pprint(data)

    # for i in range(10,40):
    #     if is_prime(i):
    #         print i
    #
