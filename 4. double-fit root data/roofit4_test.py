from ROOT import *
LineColor = RooFit.LineColor
htree = TFile.Open("root_real_data.root").Get("DecayTree")
histo = TH1F("histo","plotOn test histo",1000,3000,100)
for entry in htree:
	histo.Fill(entry.D_M)
x = RooRealVar("x","x",1830,1900)
m = RooRealVar("m","m test",300)
s = RooRealVar("s","s test",500)
m2 = RooRealVar("m2","m2 test",200)
s2 = RooRealVar("s2","s2 test",300)
g1frac = RooRealVar("g1frac","g1frac test",0.5)
g2frac = RooRealVar("g2frac","g2frac test",0.1)
hdata = RooDataHist("data","plotOn test data with x",RooArgList(x),histo)
m.setConstant(kFALSE)
s.setConstant(kFALSE)
m2.setConstant(kFALSE)
s2.setConstant(kFALSE)
model = RooGaussian("model","gauss test",x,m,s)
model2 = RooGaussian("model2","gauss2 test",x,m2,s2)
modelsum = RooAddPdf("modelsum","model+model2",RooArgList(model,model2),RooArgList(g1frac,g2frac))
frame = x.frame()
modelsum.fitTo(hdata)
hdata.plotOn(frame)
hdata.statOn(frame)
modelsum.paramOn(frame)
modelsum.plotOn(frame,LineColor(kRed))
frame.Draw()
