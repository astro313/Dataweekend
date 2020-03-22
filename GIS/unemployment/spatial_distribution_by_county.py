"""

Color based on unemployment rate in each county by matching FIPS code in .svg and update the .svg file.

"""

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

# data = pd.read_csv('unemployment09.csv')

# Read in unemployment rates
unemployment = {}
reader = csv.reader(open('unemployment09.csv'), delimiter=",")
for row in reader:
    try:
        full_FIPS = row[1] + row[2]       # state code and country code
        rate = float( row[8].strip() )    # remove white spaces
        unemployment[full_FIPS] = rate
    except:
        pass

# plot
plt.figure()
plt.title('Distribution of unemployment')
plt.hist(unemployment.values())
plt.show()

## Load County Map
# read in .svg, only care about beginning and end of path tag
# change style attribute, fill color to correspond to unemployment rate
# IMPORT XML parsing library
from bs4 import BeautifulSoup

# each county has a unique Federal information processing standard (FIPS) code
svg = open('USA_Counties_with_FIPS_and_names.svg', 'r').read()
soup = BeautifulSoup(svg, features="lxml") # , selfClosingTag=['def', 'sodipodi:namedview'])
soup.prettify()

# Find counties
paths = soup.findAll('path')

# Map colors
colors = ["#F1EEF6", "#D4B9DA", "#C994C7",
          "#DF65B0", "#DD1C77", "#980043"]
min_value = np.array(list(unemployment.values())).flatten().min()
max_value = np.array(list(unemployment.values())).flatten().max()

# normalized to between 0 and 1
plt.figure()
plt.hist((np.array(list(unemployment.values())).flatten() - min_value) / float(max_value - min_value))
plt.show()

# change fill color; changed stroke to #FFFFFF to make county borders white
# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:buttmarker-start:none;stroke-linejoin:bevel;fill:'

# loop through all paths (counties) from the .svg, find unemployment rate from unemployment dictionary based on FIPS, and color the counties
for p in paths:

    if p['id'] not in ["State_Lines", "separator"]:
        # don’t want to change style of state lines or line that separates Hawaii and Alaska from the rest of the states (open the .svg to visualize these lines)
        try:
            rate = unemployment[p['id'][5:]]
        except:
            continue

        # # hard-coded color, assuming we know the unemployment rate distribution
        # if rate > 10:
        #     color_class = 5
        # elif rate > 8:
        #     color_class = 4
        # elif rate > 6:
        #     color_class = 3
        # elif rate > 4:
        #     color_class = 2
        # elif rate > 2:
        #     color_class = 1
        # else:
        #     color_class = 0
        # color = colors[color_class]

        rate = float(rate - min_value) / float(max_value - min_value)
        # if rate > 0.83:
        #     color_class = 5
        if rate > 0.67:
            color_class = 5
        elif rate > 0.5:
            color_class = 4
        elif rate > 0.33:
            color_class = 3
        elif rate > 0.17:
            color_class = 2
        else:
            color_class = 1
        color = colors[color_class]

        try:
            p['style'] = path_style + color
        except SyntaxError:
            b = p.attrs
            b['style'] = path_style + color
            p.attrs = b
            p.attrs.update()
    else:
        # change state border line color to WHITE
        p['stroke'] = "#FFFFFF"


# Output map
f = open('US_unemployment_colored_map.svg',"w")
f.write(soup.prettify())
f.close()




