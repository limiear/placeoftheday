from datetime import datetime
from placedescriptor import get
import urllib
import json
from PIL import Image


def download(source, destiny):
    urllib.urlretrieve(source, destiny)


def draw(history, latlon, name):
    columns = get(history.get([datetime.today().date()])[0][1])
    location_map = ("http://maps.googleapis.com/maps/api/staticmap?center=%s"
                    "&zoom=2&size=200x200&maptype=roadmap&sensor=false"
                    "&markers=size:mid|color:red|label:P|%s" % (latlon, latlon))
    download(location_map, 'map.png')
    city_map = ("http://maps.googleapis.com/maps/api/staticmap?center=%s"
                "&zoom=14&size=200x200&maptype=satellite&sensor=false"
                "&markers=size:mid|color:red|label:P|%s" % (latlon, latlon))
    download(city_map, 'sat_map.png')
    result = ['map.png', 'sat_map.png']
    url = ("https://ajax.googleapis.com/ajax/services/search/"
           "images?v=1.0&q=%s photographs" % name)
    data = json.load(urllib.urlopen(url))
    images = map(lambda r: r['url'], data['responseData']['results'])
    images = filter(lambda f: f[-3:] in ['png', 'jpg', 'gif', 'bmp'], images)
    if len(images):
        picture = 'picture.%s' % images[0][-3:]
        download(images[0], picture)
        im = Image.open(picture)
        size = im.size
        ratio = size[1] / float(size[0])
        im.resize((400, int(400 * ratio)), Image.BILINEAR)
        im.save(picture)
        result.append(picture)
    return result
