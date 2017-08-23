from Utils.Constants import *
class MRXConstants(Constants):

    WEBDRIVERTIMEOUT = 12

    TIMEZONEOFFSET = 0
    TIMEPATTERN = '%d %b %Y %H:%M'

    NumberOfSelectionOnAtAnyLevel = 2
    NumberOfElementToBeExpandOnAtAnyLevel = 5

    SEGMENTSCREEN = "segment_Screen"
    SEGMENTFILTERSCREEN="filter_Screen"
    UDSCREEN= "ud_Screen"
    UDPPOPUP="udp_popup"
    POPUPSCREEN="popUp_Screen"
    EDITHEADERINEDITPOPUP = 'Edit Segment'
    CREATESEGMENT='Create Segment'
    IMPORTSEGMENT= 'Import Segment'
    INFOHEADERINPOPUP='Segment Info'
    FILTERSCREEN="filter_Screen"
    Apply_Filter='Apply Filters'
    Clear_All='Clear All'
    LFPOPUP='loadfilter_popup'
    SNFPOPUP='saveNewfilter_popup'
    ExploreScreen="explore_Screen"
    AvailableFilterList='availableFilterList'
    Logout='Logout'
    NO_FILTER='No filters'
    SearchValue='h'

    TimeRangeSpliter='-'
    NUMBEROFFILTERSCENARIO = 6

    MinimumUserConfig=15
    Source_User_Distribution='User Distribution'
    ExpectedFilterOption = ['Time Range','Measure','Segmentation Filters','Device Filters','Network Filters','Content Filters','Usage Filters']
    ExpectedQuickLinkList= ['Last 30 days','Last 7 days','Yesterday','Last 24 hours','Last 4 hours','Today','Calender']
    #ExpectedMeasure=['Volume (Upload)','Volume (Download)','Volume','# Session']
    ExpectedMeasure = ['Volume (Upload)', 'Volume (Download)', 'Volume', '# Network Session','# Web Domain Session','# IAB Session','# Contextual Session']
    ListOfFilterContainingTree=['Content Interest','Operator Data Services','Location']
    SegmentScreenTableHeaderList= ['Segment Name','User Count','Status','Source','Owner','Access','Created on','Edit/Info','Delete']
    ALL='ALL'
    REFRESH='Refresh'
    ALLLINKS = "alllinks"
    ADMIN='admin'
    NODATAMSG='No Rows To Show'
    MONTHLIST=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']