#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from twython import Twython, TwythonError
import model.database as db
from model import PlaceHistory
from grapher import draw
from placedescriptor import describe
import time
from twitter_keys import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
import random
from StringIO import StringIO
import itertools
import shelve


def twython(func):
    def func_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TwythonError as e:
            print e
    return func_wrapper


class Presenter(object):

    def __init__(self):
        self.twitter = Twython(
            APP_KEY,
            APP_SECRET,
            OAUTH_TOKEN,
            OAUTH_TOKEN_SECRET
        )
        self.intros = [
            'El lugar del dia es %s.',
            'Hoy es interesante conocer a %s.',
            '%s es lo recomendado para hoy.',
            'Disfruta de %s.',
            'Aprecia a %s.',
            'Relajate en %s.',
            'Inspirate en %s.',
        ]

    def upload_media(self, image):
        with open(image, 'rb') as photo:
            result = StringIO(photo.read())
        return result

    def tweet(self, status, images):
        time.sleep(10)
        medias = map(lambda i: self.upload_media(i), images)
        params = {'status': status}
        if not images:
            self.twitter.update_status(status=status)
        else:
            params['media'] = medias
            self.twitter.post('/statuses/update_with_media',
                              params=params)
        print status, len(status)

    @twython
    def placeoftheday_showcase(self, cache):
        history = PlaceHistory(cache)
        self.place = history.get([datetime.today().date()])[0][1]
        name, latlon = describe(self.place)
        filenames = draw(history, latlon, name)
        template = random.choice(self.intros)
        geocodes = ("https://www.google.com.ar/maps/dir/"
                    "%s//@%s,15z?hl=en" % (latlon, latlon))
        self.tweet(template % ('%s (%s)' % (name, geocodes)), filenames)

    def lotery_showcase(self, cache):
        bets = shelve.open('betsoftheday')
        all_bets = map(lambda t: (t[1][0][1:], t[0]), bets.items())
        places = {}
        for b in all_bets:
            places.setdefault(b[0], []).append(b[1])
        users = lambda l: map(lambda u: '@%s' % u, l)
        if self.place in places.keys():
            winners = places[self.place]
            self.tweet('De %i participante/s hubo %i ganador/es: %s.' %
                        (len(all_bets), len(winners), ','.join(users(winners))), [])
        else:
            keys = places.keys()
            rank = map(lambda c: rank_diff(c, self.place), keys)
            if rank:
                closest_place = keys[rank.index(min(rank))]
                self.tweet(('No hubo ganadores. '
                            'Cerca, con el #%s, estuvo/estuvieron: %s.') %
                           (closest_place,
                            ','.join(users(places[closest_place]))), [])
            else:
                self.tweet('No hubo participantes. Para participar '
                           'envíame el código hexadecimal del place '
                           'por mensaje privado.')
        # os.remove(glob.glob('betsoftheday*')[0])

    def demonstrate(self):
        cache = db.open()
        self.placeoftheday_showcase(cache)
        #if datetime.now().hour <= 8:
        #    self.lotery_showcase(cache)
        db.close(cache)


presenter = Presenter()
presenter.demonstrate()
