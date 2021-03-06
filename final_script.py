"""
LICENSE

This script is written by Auke Schuringa and Alparslan Gunaydin, Calandlyceum, Amsterdam, with the help from Jacco de Vries, NIKHEF, Amsterdam.
A special thank you to Anton van den Berg and Rutger Gast, teachers at Calandlyceum, Amsterdam.

-----------------------------------------------------------------------
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
-----------------------------------------------------------------------
"""

from ROOT import *
from lifetime import *
from datetime import datetime
from time import mktime
import math
import sys
import re

# SETTINGS	
# Name of the .root file, example: "root_real_data.root"
name_root_file = "root_real_data.root"
# Name of the tree in the .roor file to load, example: "DecayTree"
name_tree_in_root_file = "DecayTree"
# Number of parts to cut the data in, example: 12
parts_to_cut_data_in = 12
# Part of the day to cut the data in
starting_hour = 8
ending_hour = 18

hfile = TFile.Open(name_root_file)
tree = hfile.Get(name_tree_in_root_file)

def sign(num):
	if num > 0 or (num == 0 and math.atan2(num, -1.0) > 0.0):
		return 1.0
	else:
		return -1.0

def converttime(time):
	if len(str(time)) == 1 or len(str(time)) == 2:
		newtime = int(int(time)*3600*1000000)
	elif not ":" in str(time):
		unixtime = time/1000000
		newtime = datetime.fromtimestamp(unixtime).strftime("%Y-%m-%d %H:%M:%S")
	else:
		newtimeseconds = mktime(datetime.strptime(time, "%Y-%m-%d %H:%M:%S").timetuple())
		newtime = int(newtimeseconds*1000000)
	return newtime

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
	print("	Laagste tijd = {0}".format(converttime(low_time)))
	print("	Hoogste tijd = {0}".format(converttime(high_time)))
	print("Laagste en hoogste tijden berekenen - klaar")
	sys.stdout.flush()
	return (low_time, high_time)


def sort_parts():
	print("Data verdelen in twaalf stukken")
	sys.stdout.flush()
	low_time, high_time = low_high_time()
	timeblocks = (high_time - low_time)/parts_to_cut_data_in
	tijden = range(low_time, high_time, timeblocks)
	tijd_count = 0
	for tijd in tijden:
		tijd_count = tijd_count + 1
		print("	{0} | {1}".format(tijd_count, converttime(tijd)))
	print("Data verdelen in twaalf stukken - klaar")
	sys.stdout.flush()
	return tijden


def between_times(GpsTime,time_begin,time_end):
	timebegin = converttime(time_begin)
	timeend = converttime(time_end)
	by = re.search(r'([0-9][0-9][0-9][0-9])-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]',timebegin)
	bm = re.search(r'[0-9][0-9][0-9][0-9]-([0-9][0-9])-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]',timebegin)
	bd = re.search(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-([0-9][0-9]) [0-9][0-9]:[0-9][0-9]:[0-9][0-9]',timebegin)
	bh = re.search(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] ([0-9][0-9]):[0-9][0-9]:[0-9][0-9]',timebegin)
	if int(bh.group(1)) < starting_hour:
		bd = int(bd.group(1)) + 1
	ey = re.search(r'([0-9][0-9][0-9][0-9])-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]',timeend)
	em = re.search(r'[0-9][0-9][0-9][0-9]-([0-9][0-9])-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9]',timeend)
	ed = re.search(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-([0-9][0-9]) [0-9][0-9]:[0-9][0-9]:[0-9][0-9]',timeend)
	eh = re.search(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] ([0-9][0-9]):[0-9][0-9]:[0-9][0-9]',timeend)
	if int(eh.group(1)) > ending_hour:
		ed = int(ed.group(1)) - 1
#	begintime = converttime("2011-04-15 08:00:00")
	starttime = "{0}-{1}-{2} 0{3}:00:00".format(by.group(1),bm.group(1),bd.group(1),starting_hour)
	begintime = converttime(starttime)
	print(starttime)
	sys.stdout.flush()
#	endingtime = converttime("2011-10-27 18:00:00")
	endtime = "{0}-{1}-{2} {3}:00:00".format(ey.group(1),em.group(1),ed.group(1),ending_hour)
	endingtime = converttime(endtime)
	print(endtime)
	sys.stdout.flush()
	hoursinterval = converttime(10)
	day = converttime(24)
	tijden = range(begintime, endingtime, day)
	for tijd in tijden:
		if tijd <= GpsTime <= tijd + hoursinterval:
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
		if between_times(entry.GpsTime,time_begin,time_end) == True and snijden(time_begin, time_end, entry.GpsTime) == True:
			mass_histogram.Fill(entry.D_M)
			lifetime_histogram.Fill(eval(LT()))
#			print("	{0} - {1}".format(entry.GpsTime,converttime(entry.GpsTime)))
#			sys.stdout.flush()
		elif snijden(time_begin, time_end, entry.GpsTime) == True and between_times(entry.GpsTime,time_begin,time_end) == False:
			mass_histogram_b.Fill(entry.D_M)
			lifetime_histogram_b.Fill(eval(LT()))
#			print(entry.GpsTime)
#			sys.stdout.flush()
	mass_x = RooRealVar("mass_x","mass_x",1830,1900)
	lifetime_x = RooRealVar("lifetime_x","lifetime_x",-3,3)
	m = RooRealVar("m","m test",300)
	s = RooRealVar("s","s test",500)
	a = RooRealVar("a","a test",0.0001,0.0002,0.0)
	tshift = RooRealVar("thshift","tshift",0)
	alpha = RooRealVar("alpha","alpha",100)
	vlambda = RooRealVar("vlambda","vlambda",1,1,100000)
	signal = RooRealVar("g1frac","g1frac test",0.3*2700000,1,3000000)
	background = RooRealVar("g2frac","g2frac test",0.05*2700000,1,3000000)
	hdata = RooDataHist("data","plotOn test data with x",RooArgList(mass_x),mass_histogram)
	hdatalt = RooDataHist("datalt","datalt",RooArgList(lifetime_x),lifetime_histogram)
	m.setConstant(kFALSE)
	s.setConstant(kFALSE)
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
	framelt.Draw()
	return (lifetime_value, signal_value, background_value)

class D_meson:
	print("Script draaien")
	sys.stdout.flush()
	num = 0
	times = sort_parts()
	while not num == parts_to_cut_data_in:
		time_begin = times[num]
		time_end = times[num+1]
		print("	{0} | Tussen {1} en {2}".format(num+1, converttime(time_begin), converttime(time_end)))
		lifetime, signal_value, backround_value = histogram_values(time_begin, time_end)
		print("	{0} | Lifetime = {1} | Signal = {2} | Background = {4}".format(num, lifetime, signal_value, backround_value))
		sys.stdout.flush()
	print("Script draaien - klaar")
	sys.stdout.flush()
