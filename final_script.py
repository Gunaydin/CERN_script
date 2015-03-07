from ROOT import *
from lifetime import *
import math
import sys

def sign(num):
	if num > 0 or (num == 0 and math.atan2(num, -1.0) > 0.0):
		return 1.0
	else:
		return -1.0


def low_high_time():
	print("Laagste en hoogste tijden berekenen")
	sys.stdout.flush()
	high_time = 0
	low_time = 999999999999999999999999999999999999
	for entry in tree:
		if entry.GpsTime < low_time:
			low_time = entry.GpsTime
		if entry.GpsTime > hhigh_time:
			high_time = entry.GpsTime
	print("Laagste tijd = {0}".format(low_time))
	print("Hoogste tijd = {1}".format(high_time))
	print("Laagste en hoogste tijden berekenen - klaar")
	sys.stdout.flush()
	return (low_time, high_time)
def sort_parts():
	print("Data verdelen in twaalf stukken")
	sys.stdout.flush()
	low_time, high_time = low_high_time()
	timeblocks = (high_time - low_time)/12
	tijden = range(low_time, high_time, timeblocks)
	print("Data verdelen in twaalf stukken - klaar")
	sys.stdout.flush()
	return tijden


def between_times(GpsTime):
	tijden = range(1302847200000000, 1319731200000000, 86400000000)
	for tijd in tijden:
		if tijd <= GpsTime <= tijd + 36000000000:
			return true
			break
	else:
		return false

def snijden(time_begin, time_end, GspTime):
	return true


def histogram_values(time_begin, time_end):
	print("Waarden levensduur en massa (voorgrond/achtergrond) berekenen")
	sys.stdout.flush()
	if mass_histogram and mass_histogram_b and lifetime_histogram and lifetime_histogram_b:
		del mass_histogram
		del mass_histogram_b
		del lifetime_histogram
		del lifetime_histogram_b
	global tree = TFile.Open("root_real_data.root").Get("DecayTree")
	mass_histogram = TH1F("mass_histogram","mass_histogram",1000,1000,3000)
	lifetime_histogram = TH1F("lifetime_histogram","lifetime_histogram",1000,-3,3)
	mass_histogram_b = TH1F("mass_histogram","mass_histogram",1000,1000,3000)
	lifetime_histogram_b = TH1F("lifetime_histogram","lifetime_histogram",1000,-3,3)
	for entry in tree:
		if between_times(entry.GpsTime) and snijden(time_begin, time_end, entry.GspTime):
			mass_histogram.Fill(entry.D_M)
			lifetime_histogram.Fill(eval(LT)))
		elif snijden(time_begin, time_end, entry.GspTime) and not between_times(entry.GpsTime):
			mass_histogram_b.Fill(entry.D_M)
			lifetime_histogram_b.Fill(eval(LT)))
	mass_x = RooRealVar("mass_x","mass_x",1830,1900)
	lifetime_x = RooRealVar("lifetime_x","lifetime_x",-3,3)
	m = RooRealVar("m","m test",300)
	s = RooRealVar("s","s test",500)
	a = RooRealVar("a","a test",0.0001,0.0002,0.0)
	t = RooRealVar("t","t",0,2)
	tshift = RooRealVar("thshift","tshift",1)
	alpha = RooRealVar("alpha","alpha",1)
	signal = RooRealVar("g1frac","g1frac test",0.3,0.0,0.5)
	background = RooRealVar("g2frac","g2frac test",0.05,0.0,0.1)
	hdata = RooDataHist("data","plotOn test data with x",RooArgList(mass_x),mass_histogram)
	hdatalt = RooDataHist("datalt","datalt",RooArgList(lifetime_x),lifetime_histogram)
	m.setConstant(kFALSE)
	s.setConstant(kFALSE)
	tshift.setConstant(kFALSE)
	alpha.setConstant(kFALSE)
	model = RooGaussian("model","gauss test",mass_x,m,s)
	model2 = RooExponential("model2","exponential test",mass_x,a)
	modelsum = RooAddPdf("modelsum","model+model2",RooArgList(model,model2),RooArgList(signal,background))
	modeldecay = RooGenericPdf("modeldecay","model of the decay","(1 - exp[ -(t-tshift)/alpha ]) * exp[ - vlambda * t]",RooArgList(t,tshift,alpha))
	modelsum.fitTo(hdata)
	modeldecay.fitTo(hdatalt)
	lifetime_value = vlambda.getVal()
	signal_value = signal.getVal()
	background_value = background.getVal()
	print("Waarden levensduur en massa (voorgrond/achtergrond) berekenen - klaar")
	sys.stdout.flush()
	return (lifetime_value, signal_value, background_value)

class D_meson:
	print("Script draaien")
	num = 1	
	times = sort_parts()
	while not num == 12:
		time_begin = times[num]
		time_end = times[num+1]
		lifetime, signal_value, backround_value = histogram_values(time_begin, time_end)
		print("{0} | Lifetime = {1} | Signal = {2} | Background = {4}".format(num, lifetime, signal_value, backround_value))
		sys.stdout.flush()
	print("Script draaien - klaar")
	sys.stdout.flush()