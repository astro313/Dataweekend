"""

Use python to fetch a .xlsx file from a link that contains time series of corona numbers in Germany in 2020.

"""

import urllib.request

urllib.request.urlretrieve("https://python-course.eu/data1/coronacases.xlsx", "corona_germany_time_series.xlsx")