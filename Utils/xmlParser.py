import xml.etree.ElementTree as ET

class XMLParser:
    def __init__(self):
        tree = ET.parse('../configs/solutionconfig.xml')
        root = tree.getroot()
