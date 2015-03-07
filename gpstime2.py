from ROOT import *
ltime = 1302828296975552
htime = 1319760301662592
a=0
if a==0:
	difunixtime = htime - ltime
	partunixtime = difunixtime/12
	b=ltime+partunixtime
	print(b)
	if b==1319760301662592:
		c=1
