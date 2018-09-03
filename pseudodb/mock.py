import json
import decimal
import random

import time
from datetime import datetime
from enum import Enum
from collections import namedtuple
from functools import partial

FIRST_NAMES = "./lists/first.json"
LAST_NAMES = "./lists/last.json"

class MockType(Enum):
    NAME = ' '

class Name(Enum):
    FIRST = 'first'
    LAST = 'last'
    FULL = 'full'


class Mock(object):

    def __init__(self):

        mock_info = namedtuple('mock_info', 'col_type generate')
        self.mocks = {
            'firstname' : mock_info('TEXT', partial(self.generate_random_name, Name.FIRST)),
            'lastname' : mock_info('TEXT', partial(self.generate_random_name, Name.LAST)),
            'fullname' : mock_info('TEXT', partial(self.generate_random_name, Name.FULL)),
            'date' : mock_info('DATETIME', partial(self.generate_random_date)),
            'dollars' : mock_info('TEXT', partial(self.generate_dollar_amount))
        }

    def generate_random_name(self, name_type):
        
        if not isinstance(name_type, Name):
            raise TypeError('name_type must be instance of Name class')

        def get_first_name():
            with open(FIRST_NAMES) as fn:
                first_names = json.load(fn)['first']

            random_index = random.randint(1, len(first_names) + 1)
            return first_names[random_index]

        def get_last_name():
            with open(LAST_NAMES) as ln:
                last_names = json.load(ln)['last']

            random_index = random.randint(1, len(last_names) + 1)
            return last_names[random_index]

        if name_type is Name.FIRST:
            random_name = get_first_name()

        if name_type is Name.LAST:
            random_name = get_last_name()

        if name_type is Name.FULL:
            random_name = get_first_name() + " " + get_last_name()

        return random_name

    def generate_dollar_amount(self):
        random_amount = float(decimal.Decimal(random.randrange(1,1000000))/100)
        dollar_amount = "$%.2f" % random_amount

        return dollar_amount

    def generate_random_date(self):
        epoch = int(time.time())
        diff = epoch - random.randint(1, epoch + 1)
        random_date = time.strftime(
                                    '%Y-%m-%d %H:%M:%S',
                                    time.localtime(diff)
                                    )
        return(random_date)

    def get_col_type(self, mock_type):
        try:
            col_type = self.mocks[mock_type].col_type
        except:
            print('Could not find column type for mock data')

        return col_type

    def get_mock_data(self, mock_type):
        return self.mocks[mock_type].generate()
        