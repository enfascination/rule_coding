# pylint: disable = invalid-name, superfluous-parens, bad-whitespace, using-constant-test
"""
Take the raw WoW rule data and output it to a spreadsheet for manual codifying
Usage: python step1_prepcodify_minecraft.py
"""

import sys
import csv
import os
import re
import argparse
import nltk
#nltk.download('punkt')


### HELPER
### selectionSort from https://runestone.academy/runestone/books/published/pythonds/SortSearch/TheSelectionSort.html
def selectionSort(alist):
	for fillslot in range(len(alist)-1,0,-1):
		positionOfMax = 0
		for location in range(1,fillslot+1):
			if alist[location] > alist[positionOfMax]:
				positionOfMax = location
		temp = alist[fillslot]
		alist[fillslot] = alist[positionOfMax]
		alist[positionOfMax] = temp


parser = argparse.ArgumentParser()
# from http://www.knight-of-pi.org/python-argparse-massively-simplifies-parsing-complex-command-line-parameters/
# parser.add_argument('-d', '--debug', nargs='?', metavar='1..5', type=int,
#                                 choices=range(1, 5), default=2,
#                                 help='Debug level is a value between 1 and 5')
# parser.add_argument('-g', '--gui', action='store_true', 
#                                       help='Start in graphical mode if given')
parser.add_argument('-i', '--input', nargs='?', metavar='path',
                                     type=str, default='data/wow_data/',
                                     help='Take program input in the file passed after -i')
parser.add_argument('-c', '--columnheader', nargs='?', metavar='path',
                                     type=str, default='data/header.csv',
                                     help='Take program header in the file passed after -h')
parser.add_argument('-r', '--repeats', nargs='?', metavar='path',
                                     type=str, default='data/coded_blacklist.csv',
                                     help='Take program header in the file passed after -h')
parser.add_argument('-n', '--nlines', nargs='?', type=int,
                                default=200,
                                help='How many lines should be written to output?')
parser.add_argument('-t', '--tag', nargs='?', type=str,
                                default='',
                                help='how are we labeling the produced dataset?')
args = parser.parse_args()
#print( args )

### build header
header = []
with open( args.columnheader, 'r') as header_file:
    reader = csv.reader(header_file, delimiter=',')
    # pull single row from this single row file
    header = next( reader )
    # convert to dictionary of empty strings
    #  this will be the rtemplate of each row
    header = { heading : '' for heading in header }
#print(header)

# build file list
#   the most recent main rules from each server
file_list = []
data = os.getcwd() + '/data/wow_data/' ### get the current working directory
files = os.listdir(data) ### access the contents in the directory
for fi in files:
	if fi[-3::] != '.py': ### if the file isn't a python script
		if fi != '.DS_Store': ### if the file isn't a nonetype
			if fi != 'todo_servers.txt': ### could not find a way around this one bc this isn't a directory
				#print( fi )
				alist = os.listdir( data + fi ) #assign the list of files to a list
				# print('unsorted', alist) [this is how I double-checked my work)
				# now get only the main rules, no speciality rules
				alist = [ item for item in alist if re.match(r'^\d{8}.txt$', item)]
				if alist:
					#print( alist )
					selectionSort(alist) # mutator
					#print( alist[-1] )
					#print()
					#print( fi + '/' + alist[-1])
					# print('sorted', alist[-1]) [this is how I double-checked my work)
					file_list.append( args.input + fi + '/' + alist[-1])

for rulefilepath in file_list:
	#print( rulefilepath)
	communityID = rulefilepath.split('/')[-2]
	rulefile = rulefilepath.split('/')[-1]
	capture_date = rulefile.split('.')[0]
	infile = open(rulefilepath, 'r')
	url = infile.readline().strip()
	#url = url.split(' ')[1]
	writer = csv.DictWriter(sys.stdout, delimiter=',', fieldnames=header)
	line_counter = 1 # can't use enumerate because I increment this in funny ways in the loop
	#print(communityID, capture_date, url)
	for row in infile:
		rule_text = row
		if rule_text.startswith('='): # excellhandling
			rule_text = '\\' + rule_text
		rule_texts = nltk.sent_tokenize( rule_text )
		for rule_text in rule_texts:
			trow = header.copy()
			trow['domain'] = 'private_wow'
			trow['communityID'] = communityID
			trow['timestamp'] = capture_date
			trow['text'] = rule_text
			trow['lineID'] = line_counter
			trow['ref'] = url
			line_counter += 1
			writer.writerow( trow )
	if ( args.nlines  != -1 ) and ( line_counter >= args.nlines ): ### break after whole row
		break
