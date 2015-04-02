import linecache
import os
import gzip
import json
from urllib import urlopen


def get(placeslot):
    uncompressed = 'placeoftheday/worldcitiespop.txt'
    if not os.path.isfile(uncompressed):
        with open(uncompressed, 'wb') as uncom:
            with gzip.open(uncompressed + '.gz', 'rb') as com:
                uncom.writelines(com)
    line = linecache.getline(uncompressed, placeslot)
    columns = line[:-1].split(',')
    return columns


def describe(placeslot):
    columns = get(placeslot)
    data = urlopen('http://country.io/names.json')
    country = json.load(data)[columns[0].upper()]
    name = '%s, %s' % (columns[1].title(), country)
    latlon = ','.join(columns[-2:])
    return name, latlon
