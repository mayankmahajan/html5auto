class CSVReader :
    def __init__(self):
        self.csvData = self.parseCSV()

    def parseCSV(self,file=""):
        fh = open("/Users/mayank.mahajan/PycharmProjects/DataValidation/1468445330.66sourcesiteid_sourcesitetypeid=1/AGGR_total_1468445526.5840596032692.csv")
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