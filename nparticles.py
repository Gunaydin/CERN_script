from ROOT import *
import sys
import math
hfile = TFile.Open("root_real_data.root")
htree = hfile.Get("DecayTree")
a=0
b=0
def sign(num):
    if num > 0 or (num == 0 and math.atan2(num, -1.0) > 0.0):
        return 1.0
    else:
        return -1.0
for entry in htree:
	if eval("sign(entry.B_VZ - entry.D_VZ)") == 1.0:
		a = a + 1
	else:
		b = b + 1
	print(a)
	print(b)
#693661
#2778197
