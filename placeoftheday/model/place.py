from core import Variable
import random


class PlaceHistory(Variable):

    def __init__(self, cache):
        super(PlaceHistory, self).__init__(cache)
        self.name = 'places/selected'
        self.description = 'Selected places.'
        self.reference = ''

    def scrap(self, date_list):
        return [random.randrange(3173959)]
