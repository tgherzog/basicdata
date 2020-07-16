'''
Script to fetch publicly available population data and output CSV files
The script is sensitive to updates or changes in layout, so will need to be
modified periodically when new fetches are needed

See README file for sources and layout notes

Usage:
  pop.py country
  pop.py usstate [--fips=FIPS_FILE]
  pop.py uscty

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

    countries = [row['id'] for row in wb.economy.list(skipAggs=True)]
    pop = wb.data.DataFrame('SP.POP.TOTL', countries + ['WLD'], mrv=1, labels=True, skipBlanks=True)
    pop.index.rename('id', inplace=True)
    pop.rename(columns={'SP.POP.TOTL': 'population', 'Country': 'name'}, inplace=True)
    pop.sort_index().to_csv(sys.stdout, float_format='%.0f')


def get_uscounties():

    # current source: needs to be validated and updated each time
    # expected fields: SUMLEV,STATE,COUNTY,CTYNAME,POPESTIMATE2019
    url = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv'
    pop = pd.read_csv(url, encoding='ISO-8859-1').query('SUMLEV == 50')
    pop.rename(columns={'POPESTIMATE2019': 'population', 'STNAME': 'state_name'}, inplace=True)

    pop['id'] = pop['STATE'].apply(lambda x: '{:02d}'.format(x)) + pop['COUNTY'].apply(lambda x: '{:03d}'.format(x))
    pop['name'] = pop['CTYNAME'].str.replace(' County', '')

    pop.sort_values('id').to_csv(sys.stdout, index=False, columns=['id', 'name', 'population', 'state_name'])


def get_usstates():

    # current source: needs to be validated and updated each time
    # expected fields: STATE,NAME,POPESTIMATE2019
    url = 'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/state/detail/SCPRC-EST2019-18+POP-RES.csv'

    # corrected state/territory names
    renames = {'Puerto Rico Commonwealth': 'Puerto Rico'}

    meta = pd.read_csv(options['--fips'], dtype=str).set_index('fips')
    pop = pd.read_csv(url).query('STATE != 0')
    pop.rename(columns={'STATE': 'id', 'POPESTIMATE2019': 'population', 'NAME': 'name'}, inplace=True)

    # cleaning
    pop['name'] = pop['name'].apply(lambda x: renames.get(x, x))
    pop['id']   = pop['id'].apply(lambda x: '{:02d}'.format(x))
    pop['code'] = pop['id'].apply(lambda x: meta.loc[x, 'code'])

    pop.sort_values('id').to_csv(sys.stdout, index=False, columns=['id', 'name', 'population', 'code'])


if options['country']:
    get_countries()
elif options['usstate']:
    get_usstates()
elif options['uscty']:
    get_uscounties()
