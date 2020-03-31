'''
Script to fetch publicly available surface area and land area data and output CSV files
The script is sensitive to updates or changes in layout, so will need to be
modified periodically when new fetches are needed.

See README file for sources and layout notes

Usage:
  area.py --level=LEVEL [--input-dir=DIR]

Options:
  --level=LEVEL      Level to fetch (country | usstate | uscty) [default: country]

  --input-dir=DIR    Input directory [default: inputs]
'''

import pandas as pd
import wbgapi as wb
import sys
import os
import yaml

from docopt import docopt

options = docopt(__doc__)

def get_countries():

    pop = wb.data.DataFrame(['AG.LND.TOTL.K2', 'AG.SRF.TOTL.K2'], mrnev=1, labels=True, skipAggs=True, skipBlanks=True)
    pop.index.rename('id', inplace=True)
    pop.rename(columns={'AG.SRF.TOTL.K2': 'surface_area', 'AG.LND.TOTL.K2': 'land_area', 'Country': 'name'}, inplace=True)
    pop.sort_index().to_csv(sys.stdout, float_format='%.0f', columns=['name', 'surface_area', 'land_area'])


def get_areadata(level):

    # The FactFinder link above provides a user interface to download a zipped CSV file, which you must first extract
    # to the local directory
    input_file = os.path.join(options['--input-dir'], 'DEC_10_SF1_GCTPH1.US05PR.csv')

    area = pd.read_csv(input_file, encoding='ISO-8859-1').dropna(subset=['GCT_STUB.target-geo-id2'])
    area.rename(columns={'GCT_STUB.target-geo-id2': 'fips_num', 'SUBHD0301': 'surface_area', 'SUBHD0303': 'land_area', 'GCT_STUB.display-label.1': 'name'}, inplace=True)
    area.loc[area.fips_num<100,'id'] = area.loc[area.fips_num<100].fips_num.apply(lambda x: '{:02d}'.format(int(x)))
    area.loc[area.fips_num>=100,'id'] = area.loc[area.fips_num>=100].fips_num.apply(lambda x: '{:05d}'.format(int(x)))

    # convert from sq. miles to sq. km
    area[['surface_area', 'land_area']] *= 2.58999
    if level == 'usstate':
        meta = {i['fips']: i for i in yaml.safe_load(open(os.path.join(options['--input-dir'], 'usstatemeta.yaml'), 'r'))}
        area = area[area.fips_num<100]
        area['code'] = area['id'].apply(lambda x: meta[x]['code'])
        area.to_csv(sys.stdout, index=False, columns=['id', 'name', 'surface_area', 'land_area', 'code'], float_format='%.0f')
    else:
        area = area[area.fips_num>=100]
        area['name'] = area['name'].str.replace(' County', '')
        area['name'] = area['name'].str.replace(' Municipio', '')
        area['state_name'] = area['GCT_STUB.display-label'].apply(lambda x: x.split(' - ')[1])
        area.to_csv(sys.stdout, index=False, columns=['id', 'name', 'surface_area', 'land_area', 'state_name'], float_format='%.0f')


if options['--level'] == 'country':
    get_countries()
elif options['--level'] in ['usstate', 'uscty']:
    get_areadata(options['--level'])
else:
    raise ValueError('Uncrecognized level: {}'.format(options['--level']))
