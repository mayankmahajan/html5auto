
class Time:
    def __init__(self,year=2017,month=01,day=11,hour=04,min=00):

        months=["January","February","March","April","May","June","July","August","September","October","November","December"]

        self.year = str(year)
        self.month = str(months[month-1])
        self.day = str(day)
        self.hour = str(hour)
        self.min = str(min)
