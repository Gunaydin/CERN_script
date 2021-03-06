from ROOT import *
#from lifetime import *
LineColor = RooFit.LineColor
htree = TFile.Open("root_real_data.root").Get("DecayTree")
histo = TH1F("histo","plotOn test histo",1000,3000,100)
#histo2 = TH1F("histo2","decay histogram",-10,10,100)
for entry in htree:
	histo.Fill(entry.D_M)
#	LT()
#	histo2.Fill(retval)
x = RooRealVar("x","x",1830,1900)
#x2 = RooRealVar("x","x",-10,10)
m = RooRealVar("m","m test",300)
s = RooRealVar("s","s test",500)
s2 = RooRealVar("s2","s2 test",300)
s3 = RooRealVar("s3","s3 test",250)
a = RooRealVar("a","a test",0.0001,0.0002,0.0)
#tshift = RooRealVar
#alpha = RooRealVar
#vlambda = RooRealVar
g0frac = RooRealVar("point2","point2 test",0.05)
g1frac = RooRealVar("g1frac","g1frac test",1.5,0.0,0.8)
g2frac = RooRealVar("g2frac","g2frac test",0.05,0.0,0.1)
hdata = RooDataHist("data","plotOn test data with x",RooArgList(x),histo)
#hdata2 = RooDataHist("hdata2","decay data",RooArglist(x2),histo2)
m.setConstant(kFALSE)
s.setConstant(kFALSE)
a.setConstant(kFALSE)
s2.setConstant(kFALSE)
s3.setConstant(kFALSE)
model = RooGaussian("model","gaussian test",x,m,s)
model2 = RooGaussian("model2","gaussian2 test",x,m,s2)
model3 = RooGaussian("model3","gaussian3 test",x,m,s3)
modelsum = RooAddPdf("modelsum","modelsum test", RooArgList(model),RooArgList(g0frac))
model4 = RooExponential("model2","exponential test",x,a)
modelsum2 = RooAddPdf("modelsum","model+model2",RooArgList(modelsum,model4),RooArgList(g1frac,g2frac))
#modeldecay = RooGenericPdf("modeldecay","model of the decay","(1 - exp[ -(t-tshift)/alpha ]) * exp[ - vlambda * t]",RooArgList(tshift,alpha,vlambda))
frame = x.frame()
#frame2 = x2.frame()
modelsum2.fitTo(hdata)
#modeldecay.fitTo(hdata2)
hdata.plotOn(frame)
#hdata2.plotOn(frame2)
#modeldecay.plotOn(frame2)
hdata.statOn(frame)
modelsum2.paramOn(frame)
modelsum2.plotOn(frame,LineColor(kRed))
frame.Draw()
