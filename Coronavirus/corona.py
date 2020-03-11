import os
from selenium import webdriver
import pandas as pd
import numpy as np


class Coronavirus():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.get_source()
        self.get_table()

    def get_source(self):
        self.driver.get('https://www.worldometers.info/coronavirus/')

    def get_table(self):
        self.table = self.driver.find_element_by_xpath('//*[@id="main_table_countries"]/tbody')
        self.colNames = self.driver.find_element_by_xpath('//*[@id="main_table_countries"]/thead').text.split(' ')
        self.colNames[-3] += self.colNames[-2] + self.colNames[-1]
        self.colNames.remove(self.colNames[-2])
        self.colNames.remove(self.colNames[-1])
        self.Ncol = len(self.colNames)

    def get_table_all_country(self):
        # instead of reading the whole row, we will read from entry by entry
        tab = self.table.text.split('\n')
        nCountries = len(tab)

        df = None
        for i in range(1, nCountries):
            rowNum = str(i)
            row = self.table.find_elements_by_xpath('//tr[' + rowNum + ']')
            if type(row) is list and len(row) > 1:
                for kk in range(len(row)):
                    if row[kk].text.split('\n') == self.driver.find_element_by_xpath('//*[@id="main_table_countries"]/thead').text.split('\n'):
                        # same as colhead
                        continue
                    df = self.parse_row_to_dict(row[kk], df)
            elif type(row) is list and len(row) == 1:
                row = row[0]
                df = self.parse_row_to_dict(row, df)
            else:
                df = self.parse_row_to_dict(row, df)

        df = self.dict_to_df(df)
        return df

    def parse_row_to_dict(self, row, df):
        if df is None:
            df = {}

        entry = []
        for j in range(1, self.Ncol+1):
            entry.append(row.find_element_by_xpath("td[" + str(j) + "]").text)
        entry[1:] = [i.replace(',', '') for i in entry[1:]]
        entry[1:] = [i.replace('+', '') for i in entry[1:]]

        if "" in entry:
            # replace with -999
            for idx, lll in enumerate(entry):
                if lll == '':
                    entry[idx] = '-999'
        entry[1:] = [float(i) for i in entry[1:]]
        df[entry[0]] = entry[1:]
        return df

    def dict_to_df(self, df):
        df = pd.DataFrame(df).T
        self.colNames[1:] = [i.replace('\n', ' ') for i in self.colNames[1:]]
        df.columns=self.colNames[1:]
        return df


    def get_country_from_table(self, country):
        """
        get number for a given country only
        """
        country_element = self.table.find_element_by_xpath("//td[contains(text(), " + country + ")]")   # country
        row = country_element.find_element_by_xpath("./..")
        df = self.parse_row_to_dict(row, df=None)
        df = self.dict_to_df(df)
        return df


if __name__ == '__main__':
    bot = Coronavirus()
    df1 = bot.get_country_from_table('China')
    df2 = bot.get_country_from_table('USA')
    df3 = bot.get_table_all_country()

    # save
    from datetime import datetime
    dt = datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")

    df1.to_pickle('China_' + dt + '.pkl')
    df2.to_pickle('USA_' + dt + '.pkl')
    df3.to_pickle('World_' + dt + '.pkl')
