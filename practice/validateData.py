from copy import deepcopy

def validateData(data,parQuetFilePath):
        d = deepcopy(data)
        with open(parQuetFilePath,'r') as open_file:
            dataRead  = [eachline.strip('\n') for eachline in open_file.readlines()]
            print 'Data Read from CSV : ', dataRead