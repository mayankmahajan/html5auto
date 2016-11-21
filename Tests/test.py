import re
piedata=[u'MME\n8.29 Tbps',u'UNKNOWN\n6.83 Tbps',u'P-GW\n3.52 Tbps',u'S-GW\n1.96 Tbps',u'PCRF\n946.67 Gbps',u'FTP\n50']
list=[]
text="UNK"

regex=re.compile(".*(UNKNOWN).")
print regex
[m.group(0) for l in piedata for m in [regex.search(l)] if m]
       

print list
