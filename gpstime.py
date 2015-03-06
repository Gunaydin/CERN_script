from ROOT import *
tree = TFile.Open("root_real_data.root").Get("DecayTree")
ltime = 99999999999999999999999999999999999999999999999999999999999999999999999999
htime = 0
for entry in tree:
	if entry.GpsTime < ltime:
		ltime = entry.GpsTime
		print("ltime")
		print(ltime)
	if entry.GpsTime > htime:
		htime = entry.GpsTime
		print("htime")
		print(htime)
#This script can also be used
#from ROOT import *
#tree = TFile.Open("root_real_data.root").Get("DecayTree")
#ltime = 99999999999999999999999999999999999999999999999999999999999999999999999999
#for entry in tree:
#	if entry.GpsTime < ltime:
#		ltime = entry.GpsTime
#print(ltime)
