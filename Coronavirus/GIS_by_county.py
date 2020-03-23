"""

Visualize coronavirus Confirmed cases by county

"""

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

# read in FIPS code and match it to county data manually
df_ = pd.read_csv('national_county.csv', dtype='str')    # to keep leading zero in FIPS
df_ = df_[['FIPS', 'county', 'state']]

# alternatively, this has been done by USAFacts
# https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/
df = pd.read_csv('covid_confirmed_usafacts.csv')
df['countyFIPS'] = df['countyFIPS'].map('{:0>5}'.format)

# plot the lastest date
import datetime
today = datetime.date.today()
latest = today.strftime("%m/%d/%Y").lstrip('0')

while latest not in df.columns:
    today -= datetime.timedelta(days=1)
    latest = today.strftime("%m/%d/%Y").lstrip('0')

df_latest = df[['countyFIPS', latest]]


from bs4 import BeautifulSoup
svg = open('USA_Counties_with_FIPS_and_names.svg', 'r').read()
soup = BeautifulSoup(svg, features="lxml")

# Find counties
paths = soup.findAll('path')

# Map colors
colors = ["#F1EEF6", "#D4B9DA", "#C994C7",
          "#DF65B0", "#DD1C77", "#980043"]
min_value = df_latest[latest].min()
max_value = df_latest[latest].max()

# change fill color; changed stroke to #FFFFFF to make county borders white
# County style
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:buttmarker-start:none;stroke-linejoin:bevel;fill:'

# loop through all paths (counties) from the .svg
def check_countyFIPS_in_svg_path(paths, df_latest):
    blah = []
    for p in paths:
        blah.append(p['id'][5:])

    def intersection_list(l1, l2):
        l1 = list(l1)
        l2 = list(l2)
        l3 = [value for value in l1 if value in l2]
        return l3
    bb = intersection_list(blah, list(df_latest['countyFIPS']))
    assert len(bb) > 0


for p in paths:
    if p['id'] not in ["State_Lines", "separator"]:
        # don’t want to change style of state lines or line that separates Hawaii and Alaska from the rest of the states (open the .svg to visualize these lines)
        if p['id'][5:] in list(df_latest['countyFIPS']):
            # print(p['id'][5:] + " in")
            try:
                cases = df_latest[df_latest['countyFIPS'] == p['id'][5:]][latest]
            except:
                continue
        else:
            # print(p['id'][5:] + " not in")
            continue
        cases = int(cases)
        # if cases > 1000:
        #     color_class = 5
        # elif cases > 500:
        #     color_class = 4
        # elif cases > 100:
        #     color_class = 3
        # elif cases > 10:
        #     color_class = 2
        # elif cases > 5:
        #     color_class = 1
        # else:
        #     color_class = 0

        if cases > 300:
            color_class = 5
        elif cases > 100:
            color_class = 4
        elif cases > 50:
            color_class = 3
        elif cases > 10:
            color_class = 2
        elif cases > 5:
            color_class = 1
        else:
            color_class = 0

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
f = open('US_latest_colored_by_county_map.svg',"w")
f.write(soup.prettify())
f.close()


# map the time series