from ROOT import *
htree = TFile.Open("root_real_data.root").Get("DecayTree")
histo = TH1F("histo","plotOn test histo",1000,3000,100)
for entry in htree:
	histo.Fill(entry.D_M)
x = RooRealVar("x","x",1830,1900)
m = RooRealVar("m","m test",300)
s = RooRealVar("s","s test",500)
hdata = RooDataHist("data","plotOn test data with x",RooArgList(x),histo)
m.setConstant(kFALSE)
s.setConstant(kFALSE)
model = RooGaussian("model","gauss test",x,m,s)
frame = x.frame()
model.fitTo(hdata)
hdata.plotOn(frame)
model.plotOn(frame)
frame.Draw()
