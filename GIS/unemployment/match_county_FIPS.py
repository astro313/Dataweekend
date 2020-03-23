"""

Combine FIPS state and county code and save as new pandas DF

"""

import numpy as np
import pandas as pd

state = np.genfromtxt('national_county.txt', delimiter=',', usecols=0, dtype=str)
FIPS = np.genfromtxt('national_county.txt', delimiter=',', usecols=(1,2), dtype=str)
FIPS = [i[0] + i[1] for i in FIPS]
CountyName = np.genfromtxt('national_county.txt', delimiter=',', usecols=(3), dtype=str)
blah = list(zip(FIPS, CountyName, state))
df = pd.DataFrame(blah, columns=['FIPS', 'county', 'state'])

df.to_csv('national_county.csv')