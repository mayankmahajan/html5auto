class Constants(object):

    #testcase based constants
    # URL = 'https://acume-staging.guavus.com:6443/'
    # URL = 'localhost:3333'
    # URL = 'https://nrmca.guavus.com:44710/'
    # URL = "https://muralautomation.cisco.com:6443/"
    # URL = "https://scrum.jalapeno.com:6443"
    # URL = "https://uiscrummural.cisco.com:6443/"
    isOffline = True
    if isOffline:
        URL = 'localhost:8888'
    else:
        URL = "https://murala-ca.guavus.com:6443/"

    # URL = 'http://10.71.3.77/'
    # URL = 'https://nrmca.nmcc.sprintspectrum.com:6443/'
    # URL = 'https://nrmca-upgrade-setup.sprintspectrum.com:6443/'
    # URL = 'https://nrmca-perf.guavus.com:44710/'
    USERNAME = 'admin'
    PASSWORD = 'Admin@123'

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
    WEBDRIVERTIMEOUT = 6

    # Component based constants
    ## BTV
    BTV = 'BTV'
    BTVCOLUMN0 = 'BTVCOLUMN0'
    BTVCOLUMN1 = 'BTVCOLUMN1'
    BTVCOLUMN2 = 'BTVCOLUMN2'

    TIMEZONEOFFSET = -6
    TIMEPATTERN = '%d %b %Y %H:%M:%S'
    FLAGDAILY = 24
    FLAGHOURLY = 1


    # chromedriverpath = "/Users/praveen.garg1/html5automation/chromedriver/chromedriver"
    # chromedriverpath = "C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe"
    chromedriverpath = "/Users/mayank.mahajan/PycharmProjects/html5automation/chromedriver/chromedriver"

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

    ERRORBODY = "errorbody"
    ERRORCLOSE = "errorclose"
    ERRORMESSAGE = "errormessage"
    ERRORPOPUP = "error_popup"


