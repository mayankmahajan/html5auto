class Constants(object):

    #testcase based constants
    # URL = 'https://acume-staging.guavus.com:6443/'
    # URL = 'localhost:3333'
    # URL = 'https://nrmca.guavus.com:44710/'
    # URL = "https://muralautomation.cisco.com:6443/"
    # URL = "https://scrum.jalapeno.com:6443"
    # URL = "https://uiscrummural.cisco.com:6443/"

    PROJECT = "MRX"
    # PROJECT = ""
    if PROJECT == "MRX":
        byteUnits = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    else:
        byteUnits = ["", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    BROWSER = "chrome"
    # BROWSER = "ff"
    isOffline = False
    if isOffline:
        URL = 'localhost:3333'
    else:
        #URL = "https://muralautomation.cisco.com:6443"
        #URL = "https://murala-ca.guavus.com:6443"
        #URL = "https://uiscrum-mural.cisco.com:6443"
        #URL = "https://ucsd.cisco.com:7443"
        #URL="http://192.168.174.71:9080"
        URL="http://192.168.113.191:9080/app/user-distribution"
        #URL="http://192.168.192.204:28080/"
        #URL="http://192.168.195.57:28080/"
        #URL="http://192.168.162.33:9080/"
    # URL = 'http://10.71.3.77/'
    # URL = 'https://nrmca.nmcc.sprintspectrum.com:6443/'
    # URL = 'https://nrmca-upgrade-setup.sprintspectrum.com:6443/'
    # URL = 'https://nrmca-perf.guavus.com:44710/'
    USERNAME = 'admin'
    PASSWORD = 'admin123'
    #PASSWORD = 'New@1234'
    SITES = 'site_Screen'

    # SITES = 'SITES'

    NETWORKFUNCTIONS = 'nf_Screen'
    SITEINTERACTIONS = 'siteInteraction_Screen'
    INTERFACES = 'interface_Screen'
    VRF = 'vrf_Screen'
    NENE="nene_Screen"
    CONTEXTMENU = 'CONTEXTMENU'
    EXPORTTO = 'EXPORTTO'
    EXPORTTOCSV = 'EXPORTTOCSV'
    EXPORTTOSNAPSHOT = 'EXPORTTOSNAPSHOT'
    NUMBEROFFILTERSCENARIO=6

    DRILLTO = 'DRILLTO'
    DRILLTONF = 'DRILLTONF'
    DRILLTOSITE = 'DRILLTOSITE'
    DRILLTOVRF = 'DRILLTOVRF'
    DRILLTONE = "DRILLTONE"
    DRILLTOSITEINTERACTION = 'DRILLTOSITEINTERACTION'
    NETWORKELEMENTS="ne_Screen"
    DRILLTONE="DRILLTONE"
    DRILLTONENE="DRILLTONENE"
    # driver based constants
    WEBDRIVERTIMEOUT = 1

    # Component based constants
    ## BTV
    BTV = 'BTV'
    BTVCOLUMN0 = 'BTVCOLUMN0'
    BTVCOLUMN1 = 'BTVCOLUMN1'
    BTVCOLUMN2 = 'BTVCOLUMN2'

    TIMEZONEOFFSET = -6
    # TIMEPATTERN = '%d %b %Y %H:%M:%S'
    TIMEPATTERN = '%d %b %Y %H:%M'

    FLAGDAILY = 24
    FLAGHOURLY = 1
    localserver = "http://localhost:3333/index2.html"

    chromedriverpath = "/Users/praveen.garg1/html5automation/chromedriver/chromedriver"
    # chromedriverpath = "C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe"
    #chromedriverpath = "/Users/mayank.mahajan/PycharmProjects/html5automation/chromedriver/chromedriver228"
    #firefoxdriverpath = "/Users/mayank.mahajan/Downloads/geckodriver"

    # common components
    ALLBUTTONS = "allbuttons"
    ALLSELECTS = "allselects"
    ALLRADIOS = "allradios"
    ALLINPUTS = "allinputs"
    ALLSPANS = "allspans"
    ALLLABELS = "alllabels"
    ALLCIRCLES = "allcircles"
    ALLCHECKBOXES = "allcheckboxes"
    ALLLINKS = "alllinks"
    ALLIMAGES = "allimages"

    ERRORBODY = "errorbody"
    ERRORCLOSE = "errorclose"
    ERRORMESSAGE = "errormessage"
    ERRORPOPUP = "error_popup"
    ERRORBUTTON = 'button'
    INVALIDFILTER= "invalidboxwrapper"
    INVALIDFILTERBOX="invalidfilterbox"
    NODATA= "No Data"
    UM_PARENT_WORKFLOWS="Workflows"
    UM_PARENT_BULKSTATS_KPI="Bulkstats/KPI"
    REDCOLOR="#ff0000"
    WHITECOLOR="#ffffff"
    BACKGROUNDCOLOR='background-color'
    BORDERCOLOR='border-color'
    ACTIVE_STATUS='Active'
    INACTIVE_STATUS='Inactive'

    CONFIRMATIONPOPUP='confirmation_popup'
    CONFIRMATIONBODY='confirm_popup'
    CONFIRMATIONCLOSE='closeIcon'
    CONFIRMATIONMESSAGE='text'
    CONFIRMATIONHEADER='header'
    CONFIRMATIONBUTTON='button'
    LOGINSCREEN = "loginScreen"
    Maximum_Trend_Legend = 10
    TableSecltedColor='#00e0b8'

    CONFIRMFILTERPOPUP = 'confirmation_filter_popup'
    CONFIRMFILTERBODY = 'confirm_filter_popup'
    CONFIRMFILTERCLOSE = 'closeIcon'
    CONFIRMFILTERMESSAGE = 'text'
    CONFIRMFILTERHEADER = 'header'
    CONFIRMFILTERBUTTON = 'button'
    CALENDERPOPUP = "calender_popUp"


    ERRORHEADERINCONFIRMATIONPOPUP='Error'
    CONFIRMHEADERINCONFIRMFILTERPOPUP='Delete Segment'

    PercentageAllowedinDiff=0.02

    # For Mac
    Encoding='en_US.UTF-8'

    # For Window
    #Encoding='eng'
