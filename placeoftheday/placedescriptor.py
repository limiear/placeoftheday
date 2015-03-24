import linecache

def get(placeslot):
    line = linecache.getline('placeoftheday/worldcitiespop.txt', placeslot)
    columns = line[:-1].split(',')
    return columns

def describe(placeslot):
    columns = get(placeslot)
    name = columns[1].title()
    latlon = ','.join(columns[-2:])
    return name, latlon
