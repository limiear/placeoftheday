from datetime import datetime
from placedescriptor import get
import urllib
import urllib2
import json
from PIL import Image


def download(source, destiny):
    '''Store the url source content to destiny'''
    result = True
    try:
        response = urllib2.urlopen(source)
        with open(destiny, 'wb') as fo:
            fo.write(response.read())
    except Exception:
        result = False
    return result


def aquire_image(images):
    for image in images:
        picture = 'picture.%s' % image[-3:]
        if download(image, picture):
            im = Image.open(picture)
            size = im.size
            ratio = size[1] / float(size[0])
            im.resize((400, int(400 * ratio)), Image.BILINEAR)
            im.save(picture)
            return picture
    return None


def draw(history, latlon, name):
    # columns = get(history.get([datetime.today().date()])[0][1])
    location_map = ("http://maps.googleapis.com/maps/api/staticmap?center=%s"
                    "&zoom=2&size=200x200&maptype=roadmap&sensor=false"
                    "&markers=size:mid|color:red|label:P|%s" % (latlon, latlon))
    download(location_map, 'map.png')
    city_map = ("http://maps.googleapis.com/maps/api/staticmap?center=%s"
                "&zoom=14&size=200x200&maptype=satellite&sensor=false"
                "&markers=size:mid|color:red|label:P|%s" % (latlon, latlon))
    download(city_map, 'sat_map.png')
    result = ['map.png', 'sat_map.png']
    url = ("https://api.duckduckgo.com/i.js?o=json&ia=images&"
           "q=%s tourism landscape" % name)
    req = urllib.urlopen(url)
    data = json.load(req)
    images = map(lambda r: r['image'], data['results'])
    images = filter(lambda f: f[-3:] in ['png', 'jpg', 'gif', 'bmp'], images)
    picture = aquire_image(images)
    if picture:
        result.insert(0, picture)
    return result
