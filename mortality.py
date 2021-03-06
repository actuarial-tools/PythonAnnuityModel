import pandas as pd
from enum import Enum
import pathlib


class ProductTypes(Enum):
    ImmAnn = 1
    EqRel = 2


class Mortality(object):

    def __init__(self, mortality_file_name):
        self.curve = pd.read_csv(str(pathlib.Path().absolute()) + '/assumptions/' + str(mortality_file_name) + '.csv', index_col=[0,1,2])

    # Returns mortality curve value (annual q_x value) for given lookup values
    def qxpa(self, age, sex, product, duration):
        try:
            if duration < self.select_periods or self.select_periods == 0:
                return float(self.curve.loc[age, sex, product.name]['qx' + str(duration)])
            else:
                return float(self.curve.loc[age, sex, product.name]['qx' + str(self.select_periods) + 'p'])
        except KeyError:
            return 1

    # Returns mortality curve value (annual q_x value) for given lookup values
    def qxpm(self, age, sex, product, duration):
        return 1 - (1 - self.qxpa(age, sex, product, duration))**(1/12)

    # Returns the number of select periods contained in the mortality data file
    @property
    def select_periods(self):
        return self.curve.shape[1] - 1

    # Returns the greatest age for which there is mortality data in file
    @property
    def age_cap(self):
        return max(self.curve._get_label_or_level_values('age'))
