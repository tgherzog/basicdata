'''
Script to fetch publicly available population data and output CSV files
The script is sensitive to updates or changes in layout, so will need to be
modified periodically when new fetches are needed

See README file for sources and layout notes

Usage:
  centroid.py country
  centroid.py usstate [--fips=FIPS_FILE]
  centroid.py uscty

Options:
  --fips=FIPS_FILE   Path to FIPS file [default: data/usstates.csv]

'''

import pandas as pd
import wbgapi as wb
import sys
import os

from docopt import docopt

options = docopt(__doc__)

def get_countries():

    cen = wb.economy.DataFrame(skipAggs=True)
    cen.index.rename('id', inplace=True)
    cen.rename(columns={'longitude': 'long', 'latitude': 'lat'}, inplace=True)
    cen.sort_index().to_csv(sys.stdout, columns=['name', 'long', 'lat'])


def get_uscounties():

    # current source: needs to be validated and updated each time
    url = 'https://www2.census.gov/geo/docs/reference/cenpop2010/county/CenPop2010_Mean_CO.txt'
    cen = pd.read_csv(url, encoding='ISO-8859-1')
    cen.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'long', 'STNAME': 'state_name', 'COUNAME': 'name'}, inplace=True)

    cen['id'] = cen['STATEFP'].apply(lambda x: '{:02d}'.format(x)) + cen['COUNTYFP'].apply(lambda x: '{:03d}'.format(x))

    cen.sort_values('id').to_csv(sys.stdout, index=False, columns=['id', 'name', 'long', 'lat', 'state_name'])


def get_usstates():

    # current source: needs to be validated and updated each time
    url = 'https://www2.census.gov/geo/docs/reference/cenpop2010/CenPop2010_Mean_ST.txt'

    meta = pd.read_csv(options['--fips'], dtype=str).set_index('fips')
    cen = pd.read_csv(url)
    cen.rename(columns={'STATEFP': 'id', 'LATITUDE': 'lat', 'LONGITUDE': 'long', 'STNAME': 'name'}, inplace=True)

    # cleaning
    cen['id']   = cen['id'].apply(lambda x: '{:02d}'.format(x))
    cen['code'] = cen['id'].apply(lambda x: meta.loc[x, 'code'])

    cen.sort_values('id').to_csv(sys.stdout, index=False, columns=['id', 'name', 'long', 'lat', 'code'])


if options['country']:
    get_countries()
elif options['usstate']:
    get_usstates()
elif options['uscty']:
    get_uscounties()
