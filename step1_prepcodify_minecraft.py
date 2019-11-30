# pylint: disable = invalid-name, superfluous-parens, bad-whitespace, using-constant-test
"""
Take the raw Minecraft sign data and output it to a spreadsheet for manual codifying
Usage: python step1_prepcodify_minecraft.py
"""

import sys
import csv
import argparse
import nltk
#nltk.download('punkt')

parser = argparse.ArgumentParser()
# from http://www.knight-of-pi.org/python-argparse-massively-simplifies-parsing-complex-command-line-parameters/
# parser.add_argument('-d', '--debug', nargs='?', metavar='1..5', type=int,
#                                 choices=range(1, 5), default=2,
#                                 help='Debug level is a value between 1 and 5')
# parser.add_argument('-g', '--gui', action='store_true', 
#                                       help='Start in graphical mode if given')
parser.add_argument('-i', '--input', nargs='?', metavar='path',
                                     type=str, default='data/mcsigns_full.csv',
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

#### build blacklist
#communities_coded = []
#with open( args.repeats, 'r') as blacklist_file:
#    reader = csv.DictReader(blacklist_file, delimiter=',')
#    for row in reader:
#        domain = row['domain']
#        community = row['communityID']
#        communities_coded.append( domain+'_'+community )
#print( communities_coded )

with open(args.input, 'r') as csv_infile:
    reader = csv.DictReader(csv_infile, delimiter=',')
    writer = csv.DictWriter(sys.stdout, delimiter=',', fieldnames=header)
    line_counter = 1 # can't use enumerate because I incremenet this in funny ways in the loop
    for row in reader:
        rule_text = row['text']
        rule_text = rule_text.replace(r'\\', ' ') # for minecraft
        if rule_text.startswith('='):
             rule_text = '\\' + rule_text
        rule_texts = nltk.sent_tokenize( rule_text )
        for rule_text in rule_texts:
            trow = header.copy()
            trow['domain'] = 'minecraft'
            if row['port'] == '25565':
                trow['communityID'] = row['host']
            else:
                trow['communityID'] = row['host'] + row['port']
            trow['text'] = rule_text
            trow['lineID'] = line_counter
            line_counter += 1
            writer.writerow( trow )
        if ( args.nlines  != -1 ) and ( line_counter >= args.nlines ): ### break after whole row
            break
