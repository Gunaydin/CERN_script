from ROOT import *
hfile = TFile.Open("root_data.root")
htree = hfile.Get("b2D0MuXDst_DTF/DecayTree")
hist1 = TH1F("hist1","Auke + Alparslan Histogram D_M, 0.05 <= D_IP >= 0.4",1000,3000,100)
for entry in htree:
  if entry.D_IP >= 0.05 and entry.D_IP <= 0.4:
    hist1.Fill(entry.D_M)

hist1.Draw()
