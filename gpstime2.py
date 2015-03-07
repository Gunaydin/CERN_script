from ROOT import *
ltime = 1302828296975552
htime = 1319760301662592
difunixtime = htime - ltime
partunixtime = difunixtime/12
while not b == 1319760301662592:
	b=ltime+partunixtime
	print(b)
