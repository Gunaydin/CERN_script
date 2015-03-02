from ROOT import *
htree = TFile.Open("root_data.root").Get("b2D0MuXDst_DTF/DecayTree")
histo = TH1F("histo","plotOn test histo",1000,3000,100)
for entry in htree:
	histo.Fill(entry.D_M)
x = RooRealVar("x","x",1830,1900)
hdata = RooDataHist("data","plotOn test data with x",RooArgList(x),histo)
frame = x.frame()
hdata.plotOn(frame)
frame.Draw()
