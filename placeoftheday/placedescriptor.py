import linecache
import os
import gzip


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
    name = columns[1].title()
    latlon = ','.join(columns[-2:])
    return name, latlon
