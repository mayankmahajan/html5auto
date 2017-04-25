from Utils.utility import *

for i in [0,1,2]:
    checkEqualAssert("ex"+str(i),"e"+str(i),message="sadads"+str(i))

for i in [0,1,2]:
    checkEqualAssert("e"+str(i),"e"+str(i),message="sadads"+str(i))

for i in [0,1,2]:
    checkEqualAssert("ex"+str(i),"1ex"+str(i),message="sadads"+str(i))

for i in [0,1,2]:
    checkEqualAssert("ex"+str(i),"ex"+str(i),message="sadads"+str(i))

