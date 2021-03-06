'''
Script to fetch publicly available surface area and land area data and output CSV files
The script is sensitive to updates or changes in layout, so will need to be
modified periodically when new fetches are needed.

See README file for sources and layout notes

Usage:
  area.py country
  area.py usstate --src=SRC_FILE [--fips=FIPS_FILE]
  area.py uscty   --src=SRC_FILE [--fips=FIPS_FILE]

Options:
  --src=SRC_FILE     Source file
  --fips=FIPS_FILE   Path to FIPS file [default: data/usstates.csv]

'''

import pandas as pd
import wbgapi as wb
import sys
import os

from docopt import docopt

options = docopt(__doc__)

def get_countries():

    countries = [row['id'] for row in wb.economy.list(skipAggs=True)]
    pop = wb.data.DataFrame(['AG.LND.TOTL.K2', 'AG.SRF.TOTL.K2'], countries + ['WLD'], mrnev=1, labels=True, skipBlanks=True)
    pop.index.rename('id', inplace=True)
    pop.rename(columns={'AG.SRF.TOTL.K2': 'surface_area', 'AG.LND.TOTL.K2': 'land_area', 'Country': 'name'}, inplace=True)
    pop.sort_index().to_csv(sys.stdout, float_format='%.0f', columns=['name', 'surface_area', 'land_area'])


def get_areadata(usstate):

    # The FactFinder link above provides a user interface to download a zipped CSV file, which you must first extract
    # to the local directory

    area = pd.read_csv(options['--src'], encoding='ISO-8859-1').dropna(subset=['GCT_STUB.target-geo-id2'])
    area.rename(columns={'GCT_STUB.target-geo-id2': 'fips_num', 'SUBHD0301': 'surface_area', 'SUBHD0303': 'land_area', 'GCT_STUB.display-label.1': 'name'}, inplace=True)
    area.loc[area.fips_num<100,'id'] = area.loc[area.fips_num<100].fips_num.apply(lambda x: '{:02d}'.format(int(x)))
    area.loc[area.fips_num>=100,'id'] = area.loc[area.fips_num>=100].fips_num.apply(lambda x: '{:05d}'.format(int(x)))

    # convert from sq. miles to sq. km
    area[['surface_area', 'land_area']] *= 2.58999
    if usstate:
        meta = pd.read_csv(options['--fips'], dtype=str).set_index('fips')
        area = area[area.fips_num<100]
        area['code'] = area['id'].apply(lambda x: meta.loc[x, 'code'])
        area.to_csv(sys.stdout, index=False, columns=['id', 'name', 'surface_area', 'land_area', 'code'], float_format='%.0f')
    else:
        area = area[area.fips_num>=100]
        area['name'] = area['name'].str.replace(' County', '')
        area['name'] = area['name'].str.replace(' Municipio', '')
        area['state_name'] = area['GCT_STUB.display-label'].apply(lambda x: x.split(' - ')[1])
        area.to_csv(sys.stdout, index=False, columns=['id', 'name', 'surface_area', 'land_area', 'state_name'], float_format='%.0f')


if options['country']:
    get_countries()
elif options['usstate'] or options['uscty']:
    get_areadata(options['usstate'])
