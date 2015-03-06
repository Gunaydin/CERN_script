sigfrac = RooRealVar("sigfrac","sigfrac", 0.7, 0.5, 1.)
  
  gauss    = RooGaussian("gauss","gauss",x,mean,gswidth)
  CB       = RooCBShape("CB","CB",x,mean, cbwidth, cba,cbn)
  sigmodel = RooAddPdf("sigmodel","Signal model", RooArgList(CB, gauss), RooArgList(sigfrac))
  bgmodel  = RooChebychev("bgmodel","Background model",x,RooArgList(chebv))

  Nsig = RooRealVar("Nsig","Nsig", nentries*0.09, 0, 10000000)
  Nbkg = RooRealVar("Nbkg","Nbkg", nentries*0.04, 0, 10000000)
  fullPdf = RooAddPdf("fullPdf","fullPdf", RooArgList(sigmodel, bgmodel), RooArgList(Nsig,Nbkg)) 

  data = RooDataHist( "data", "data", RooArgList(x), hist )
  
  fullPdf.fitTo( data )

  fitYield = Nsig.getVal()
  fitError = Nsig.getError()
