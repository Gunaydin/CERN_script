from ROOT import *
from lifetime import *
import math
import functools
LineColor = RooFit.LineColor
htree = TFile.Open("root_real_data.root").Get("DecayTree")
histo = TH1F("histo","plotOn test histo",1000,1000,3000)
histolt = TH1F("histolt","plotOn test histolt",10000,-3,3)
def sign(num):
	if num > 0 or (num == 0 and math.atan2(num, -1.0) > 0.0):
		return 1.0
	else:
		return -1.0
for entry in htree:
	histo.Fill(entry.D_M)
#	print(eval(LT()))
	histolt.Fill(eval(LT()))
x = RooRealVar("x","x",1830,1900)
x2 = RooRealVar("x2","x2",-3,3)
m = RooRealVar("m","m test",300)
s = RooRealVar("s","s test",500)
a = RooRealVar("a","a test",0.0001,0.0002,0.0)
t = RooRealVar("t","t",0,2)
tshift = RooRealVar("thshift","tshift",0)
alpha = RooRealVar("alpha","alpha",0)
g1frac = RooRealVar("g1frac","g1frac test",0.3,0.0,0.5)
g2frac = RooRealVar("g2frac","g2frac test",0.05,0.0,0.1)
hdata = RooDataHist("data","plotOn test data with x",RooArgList(x),histo)
hdatalt = RooDataHist("datalt","datalt",RooArgList(x2),histolt)
m.setConstant(kFALSE)
s.setConstant(kFALSE)
tshift.setConstant(kFALSE)
alpha.setConstant(kFALSE)
model = RooGaussian("model","gauss test",x,m,s)
model2 = RooExponential("model2","exponential test",x,a)
modelsum = RooAddPdf("modelsum","model+model2",RooArgList(model,model2),RooArgList(g1frac,g2frac))
modeldecay = RooGenericPdf("modeldecay","model of the decay","(1 - exp[ -(t-tshift)/alpha ]) * exp[ - lambda * t]",RooArgList(t,tshift,alpha))
frame = x.frame()
framelt = x2.frame()
modelsum.fitTo(hdata)
modeldecay.fitTo(hdatalt)
hdata.plotOn(frame)
hdata.statOn(frame)
hdatalt.plotOn(framelt)
hdatalt.statOn(framelt)
modelsum.paramOn(frame)
modelsum.plotOn(frame,LineColor(kRed))
modeldecay.plotOn(framelt)
