# pylint: disable = invalid-name, superfluous-parens, bad-whitespace, using-constant-test
"""
Takes data that has already been coded and generates a blacklist of sites not to put back into a dataset
"""

import sys
import csv
import argparse

parser = argparse.ArgumentParser()
# from http://www.knight-of-pi.org/python-argparse-massively-simplifies-parsing-complex-command-line-parameters/
# when the time comes: scale this to take several files: https://gist.github.com/89465127/5273149
parser.add_argument('-i', '--input', metavar='path',
                                     type=str, nargs=argparse.ONE_OR_MORE,
                                     default='data/coded/rules_data_codifying - statements_MASTER.csv',
                                     help='Take program input in the file passed after -i')
args = parser.parse_args()

communities_seen = []
with open(args.input, 'r') as csv_infile:
    reader = csv.DictReader(csv_infile, delimiter=',')
    writer = csv.DictWriter(sys.stdout, delimiter=',', fieldnames=('domain', 'communityID'))
    writer.writeheader()
    for i, row in enumerate(reader):
        domain = row['domain']
        community = row['communityID']
        id = domain + '_' + community
        if id not in communities_seen:
            trow = {'domain' : row['domain'], 'communityID' : row['communityID']}
            communities_seen.append( id )
            writer.writerow( trow )
