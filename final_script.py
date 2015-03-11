from ROOT import *
from lifetime import *
import math
import sys

tree = TFile.Open("root_real_data.root").Get("DecayTree")

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
		if entry.GpsTime > high_time:
			high_time = entry.GpsTime
	print("	Laagste tijd = {0}".format(low_time))
	print("	Hoogste tijd = {0}".format(high_time))
	print("Laagste en hoogste tijden berekenen - klaar")
	sys.stdout.flush()
	return (low_time, high_time)


def sort_parts():
	print("Data verdelen in twaalf stukken")
	sys.stdout.flush()
	low_time, high_time = low_high_time()
	timeblocks = (high_time - low_time)/12
	tijden = range(low_time, high_time, timeblocks)
	tijd_count = 0
	for tijd in tijden:
		tijd_count = tijd_count + 1
		print("	{0} | {1}".format(tijd_count, tijd))
	print("Data verdelen in twaalf stukken - klaar")
	sys.stdout.flush()
	return tijden


def between_times(GpsTime):
	tijden = range(1302847200000000, 1319731200000000, 86400000000)
	for tijd in tijden:
		if tijd <= GpsTime <= tijd + 36000000000:
			return True
			break
	else:
		return False

def snijden(time_begin, time_end, GpsTime):
	if time_begin <= GpsTime <= time_end:
		return True
	else:
		return False


def histogram_values(time_begin, time_end):
	print("Waarden levensduur en massa (voorgrond/achtergrond) berekenen")
	sys.stdout.flush()
	mass_histogram = None
	lifetime_histogram = None
	mass_histogram_b = None
	lifetime_histogram_b = None
	mass_histogram = TH1F("mass_histogram","mass_histogram",1000,1830,1900)
	lifetime_histogram = TH1F("lifetime_histogram","lifetime_histogram",1000,-3,3)
	mass_histogram_b = TH1F("mass_histogram","mass_histogram",1000,1830,1900)
	lifetime_histogram_b = TH1F("lifetime_histogram","lifetime_histogram",1000,-3,3)
	for entry in tree:
		if between_times(entry.GpsTime) == True and snijden(time_begin, time_end, entry.GpsTime) == True:
			mass_histogram.Fill(entry.D_M)
			lifetime_histogram.Fill(eval(LT()))
			print("	{0}".format(entry.GpsTime))
			sys.stdout.flush()
		elif snijden(time_begin, time_end, entry.GpsTime) == True and between_times(entry.GpsTime) == False:
			mass_histogram_b.Fill(entry.D_M)
			lifetime_histogram_b.Fill(eval(LT()))
			print(entry.GpsTime)
			sys.stdout.flush()
	mass_x = RooRealVar("mass_x","mass_x",1830,1900)
	lifetime_x = RooRealVar("lifetime_x","lifetime_x",-3,3)
	m = RooRealVar("m","m test",300)
	s = RooRealVar("s","s test",500)
	a = RooRealVar("a","a test",0.0001,0.0002,0.0)
	t = RooRealVar("t","t",0,2)
	tshift = RooRealVar("thshift","tshift",0)
	alpha = RooRealVar("alpha","alpha",100)
	vlambda = RooRealVar("vlambda","vlambda",1)
	signal = RooRealVar("g1frac","g1frac test",0.3*2700000,1,3000000)
	background = RooRealVar("g2frac","g2frac test",0.05*2700000,1,3000000)
	hdata = RooDataHist("data","plotOn test data with x",RooArgList(mass_x),mass_histogram)
	hdatalt = RooDataHist("datalt","datalt",RooArgList(lifetime_x),lifetime_histogram)
	m.setConstant(kFALSE)
	s.setConstant(kFALSE)
	vlambda.setConstant(kFALSE)
	model = RooGaussian("model","gauss test",mass_x,m,s)
	model2 = RooExponential("model2","exponential test",mass_x,a)
	modelsum = RooAddPdf("modelsum","model+model2",RooArgList(model,model2),RooArgList(signal,background))
	modeldecay = RooGenericPdf("modeldecay","model of the decay","(1 - exp[ -(lifetime_x-tshift)/alpha ]) * exp[ - vlambda * lifetime_x]",RooArgList(lifetime_x,tshift,alpha,vlambda))
	frame = mass_x.frame()
	framelt = lifetime_x.frame()
	modelsum.fitTo(hdata)
	modeldecay.fitTo(hdatalt)
	hdatalt.plotOn(framelt)
	hdatalt.statOn(framelt)
	modeldecay.plotOn(framelt)
	lifetime_value = vlambda.getVal()
	signal_value = signal.getVal()
	background_value = background.getVal()
	print("Waarden levensduur en massa (voorgrond/achtergrond) berekenen - klaar")
	sys.stdout.flush()
	return (lifetime_value, signal_value, background_value)

class D_meson:
	print("Script draaien")
	sys.stdout.flush()
	num = 0
	times = sort_parts()
	while not num == 12:
		time_begin = times[num]
		time_end = times[num+1]
		print("	{0} | GpsTime(UnixTime) tussen {1} en {2}".format(num+1, time_begin, time_end))
		lifetime, signal_value, backround_value = histogram_values(time_begin, time_end)
		print("	{0} | Lifetime = {1} | Signal = {2} | Background = {4}".format(num, lifetime, signal_value, backround_value))
		sys.stdout.flush()
	print("Script draaien - klaar")
	sys.stdout.flush()
