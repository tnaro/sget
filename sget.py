#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sget.py
#  
#  Copyright 2013 stefan Klinkhammer
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import urllib2
import re
from Tkinter import Tk

def extractlinks(a):
	## go through all the links and give all share-online links
	match = re.findall(r"http\:\/\/download.serienjunkies.org\/.*share-online.biz",a)
	b = [[],0]
	for j in match:
		b[0].append(j[:j.find(" target=")-1])
	
	# find also the latest episode available. We have to go this way, as there are sometimes something like SXXE00, crap...
	match = re.findall(r"S\d\dE\d\d",a)
	for j in match:
		b[1] = max(j[4:],b[1])

	return b

def main():
	sc = raw_input("Insert the serienjunkies season page >> ")
	if sc[len(sc)-1] == '/':
		sc = sc[:len(sc)-1] 

	try:
		req = urllib2.Request(sc)
		req.add_header('User-agent','Mozilla/5.0')
		openCon = urllib2.urlopen(req)
		
		source = openCon.read()
		#print source
		print "... done."
	except:
		print "Unexpected error:", sys.exc_info()[0]
		return 0

	## Code fetched, now search for the precious download links!
	# Every download link begins with http://download.serienjunkies.org/ and before
	# that there is the bracket which indicates the size

	lengths = re.split('Dauer:</strong> \*{5} | <strong>Größe:</strong> ', source)

	# First part hasn't any links
	# From then on, the first characters describe the size, now we need to filter 
	# the links each time and put them into a dictionary

	lts = {}
	for sizes in lengths:
		if sizes[:10].find("MB") != -1:
			lts[sizes[:sizes[:10].find("MB")+2]] = extractlinks(sizes)
		else:
			continue
	
	# Filter for complete shows
	cnt = [[],0]
	for maxSers in lts.keys():
		if lts[maxSers][1] > cnt[1]:
			cnt[1] = lts[maxSers][1]
			cnt[0] = [maxSers]
		elif lts[maxSers][1] == cnt[1]:
			cnt[0].append(maxSers)

	# Choose one of the complete filesizes
	print "Choose which filesize to download:"
	for szs in cnt[0]:
		print szs

	cpy = raw_input("Your choice (EXACT WORDING INCLUDING 'MB': ")

	#transform the list into a string, depending if decided for final or not
	
	if cpy == "final":
		print "latest episodes in the following sizes:"
		for szs in cnt[0]:
			print szs
		latest = raw_input("Your choice (EXACT WORDING INCLUDING 'MB': ")
		final = lts[latest][0][len(lts[latest][0])-1]

	else:
		final = ""
		for el in lts[cpy][0]:
			final += el +"\n"

	print final


	

	# use TKinter to put the links into clipboard
	#r = Tk()
	#r.withdraw()
	#r.clipboard_clear()
	#r.clipboard_append(final)
	#r.destroy()

	print "\n\nAlso copied to clipboard ;-)\n\n"


if __name__ == '__main__':
	main()

