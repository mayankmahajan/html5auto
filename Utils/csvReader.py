class CSVReader :
    def __init__(self,file="/Users/mayank.mahajan/PycharmProjects/DataValidation/1468445330.66sourcesiteid_sourcesitetypeid=1/AGGR_total_1468445526.5840596032692.csv"):
        self.csvData = self.parseCSV(file)
        pass

    def parseCSV(self,file="/Users/mayank.mahajan/PycharmProjects/DataValidation/1468445330.66sourcesiteid_sourcesitetypeid=1/AGGR_total_1468445526.5840596032692_test.csv"):
        fh = open(file)
        a = fh.readlines()
        # print a
        keys = a[0].split(',')
        d = {}
        for i in range(1,len(a)):
            d1 = {}
            for j in range(1,len(keys)):
                d1[keys[j]] = a[i].split(',')[j]

            d[a[i].split(',')[0]] = d1
        print d
        return d

    def createPath(self,stattime,endtime,screen_name,filters):
        pass

# x = CSVReader()
# print x.parseCSV
# print x.parseCSV()
