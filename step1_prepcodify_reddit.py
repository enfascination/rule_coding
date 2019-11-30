# pylint: disable = invalid-name, superfluous-parens, bad-whitespace, using-constant-test
"""
Take the raw Reddit sign data and output it to a spreadsheet for manual codifying
Usage: python step1_prepcodify_minecraft.py
"""

import sys
import pprint
import csv
import json
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
                                     type=str, default='data/RedditRulesScraperOutput.txt',
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

with open(args.input, 'r') as jsonl_infile:
    writer = csv.DictWriter(sys.stdout, delimiter=',', fieldnames=header)
    line_counter = 1 # can't use enumerate because I increment this in funny ways in the loop
    for row in  jsonl_infile: ### for each subreddit
        jrow = json.loads( row )
        for rule in jrow['rules']: ### for each rule in the sub
            rule_text = rule['description']
            ### string handling
            rule_text = rule_text.replace(r'"', "'") # for reddit: lots of quotes to deal with
            #rule_text = rule_text.replace(r'\r', r'\n') # wierd newlines
            ### aiding tokenizer
            rule_text = rule_text.replace(r'.**', '. ') # for reddit: sentences followed by markdown
            rule_text = rule_text.replace(r'.*', '. ') # for reddit
            rule_text = rule_text.replace(r'\n\n**', '. ') # for reddit: double \n+bullets instead of .'s
            rule_text = rule_text.replace(r'\n\n*', '. ') # for reddit
            rule_text = rule_text.replace(r'\n\n-', '. ') # for reddit
            rule_text = rule_text.replace(r'.\n\n', '. ') # for reddit
            rule_text = rule_text.replace(r'\n\n', '. ') # for reddit
            rule_text = rule_text.replace('\n\n', '. ') # for reddit ### not sure why this catches things the above don't
            rule_text = rule_text.replace(r'\n**', '. ') # for reddit
            rule_text = rule_text.replace(r'\n*', '. ') # for reddit
            rule_text = rule_text.replace(r'\n', ' ') # for reddit
            rule_texts = nltk.sent_tokenize( rule_text )
            for rule_text in rule_texts: ### for each institutional statement in the rule
                trow = header.copy()
                trow['domain'] = 'reddit'
                trow['communityID'] = 'r/' + jrow['sub']
                trow['timestamp'] = rule['createdUtc']
                trow['ref'] = 'https://www.reddit.com/' + trow['communityID']
                trow['context'] = rule['shortName']
                trow['text'] = rule_text
                trow['lineID'] = line_counter
                line_counter += 1
                writer.writerow( trow )
                if False and line_counter == 85:
                    print(trow)
                    print(rule)
                    print(rule['description'])
                    print(rule_texts)
                    print(rule_text)
                    print("REALLY", r'\n\n' in rule_text)
                    print("REALLY", r'\n' in rule_text)
                    print("REALLY", '\\n' in rule_text)
                    print("REALLY", '\n\n' in rule_text)
                    print("REALLY", '\n' in rule_text)
                    print("REALLY", r'\r' in rule_text)
        if ( args.nlines != -1 ) and ( line_counter >= args.nlines ): ### break after a whole sub
            break
