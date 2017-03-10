from classes.Components.TimeRangeComponentClass import *

#quicklinks=TimeRangeComponentClass().configmanager.getAllNodeElements("wizardquicklinks","wizardquicklink")

# for i in range(0,5):
#     for e in qList:
#        print qs[e]
        # print qs[e]['locatorText']
        # print TimeRangeComponentClass().getLabel(e, stEtCombID=str(i))

print TimeRangeComponentClass().getAllquicklinkLable(flag=Constants.FLAGHOURLY,stEtCombID='0')

# for i in range(0,5):
#     for quicklink in quicklinks:
#         print quicklink
#         print TimeRangeComponentClass().getLable(quicklink,stEtCombID=str(i))


#        quicklink = 'NA'
 #       quicklinks = {}
  #      qList = TimeRangeComponentClass().configmanager.getAllNodeElements("wizardquicklinks1", "wizardquicklink")

#        quicklink[qList[0]] =

 #       def getTodayLabel():
 #
 #            if int(h) == 0:
 #                h=24
            # if (etepoch - stepoch)<= int(h)*3600 :
            #     return True, stime.datestring + "  " + etime.datestring
            # else:
            #     return True, time.strftime('%Y-%m-%d %H:%M', time.localtime(etepoch  - (3600 * (int(h) + Constants.TIMEZONE))))+ "  " + etime.datestring
        #
        # if quicklink == "today" :
        #     getTodayLabel()

                # if int(h) == 0:
                #     h=24
                # if (etepoch - stepoch)<= int(h)*3600 :
                #     return True, stime.datestring + "  " + etime.datestring
                # else:
                    # return True, time.strftime('%Y-%m-%d %H:%M', time.localtime(etepoch  - (3600 * (int(h) + Constants.TIMEZONE))))+ "  " + etime.datestring

        # elif quicklink == "yesterday":
        #     if int(h) == 0:
        #         h=24
            # if (etepoch - stepoch) <= int(h)*3600:
            #     return False,""
            # else:
            #         if (etepoch - stepoch) > (int(h)+24)*3600 :
            #             return True,time.strftime('%Y-%m-%d %H:%M', time.localtime(etepoch  - (3600 * (int(h) + 24 + Constants.TIMEZONE)))) + "  " + time.strftime('%Y-%m-%d %H:%M', time.localtime(etepoch  - (3600 * (int(h) + Constants.TIMEZONE))))
                    # else:
                    #     return True,stime.datestring + "  " + time.strftime('%Y-%m-%d %H:%M', time.localtime(etepoch - (3600 * (int(h) + Constants.TIMEZONE))))

