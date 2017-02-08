
class Time:
    def __init__(self,year=2017,month=01,day=11,hour=04,min=00):

        months=["January","February","March","April","May","June","July","August","September","October","November","December"]

        self.year = self.st(year)
        self.month = self.st(months[int(month)-1])
        self.day = self.st(day)
        self.hour = self.st(hour)
        self.min = self.st(min)

        self.datestring = self.st(year)+"-"+self.st(month)+"-"+self.st(day)+" "+self.st(hour)+":"+self.st(min)

        # sample datestring from reportwizard 2017-01-24 00:00

    def st(self,string):
        return "0" +str(string) if len(str(string))==1 else str(string)
