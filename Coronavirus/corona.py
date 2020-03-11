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


    def get_table_all_country(self):
        tab = self.table.text
        self.tab_splited_by_country = tab.split('\n')
        # for each row, split by calling get_number_per_row_from_table(), put into dataframe
        df = pd.Series()
        for rr in self.tab_splited_by_country:
            s = self.get_number_per_row_from_table(rr)
            df = pd.concat([df, s], axis=1)
            # sdf[s[0]]
        df = df.T.loc[1:]
        df = df.reset_index()
        df = df.drop(['index'], axis=1)
        assert len(df.columns) == 8
        df = df.set_index('country')
        return df

    def __combine_splited_country_name(self):
        try:
            float(self.data[1])
        except ValueError:
            self.data[0] += self.data[1]
            self.data.remove(self.data[1])
            self.__combine_splited_country_name(1)

    def get_number_per_row_from_table(self, row):
        import types
        if type(row) is types.UnicodeType:
            data = row.split(" ")
        else:
            # row is selenium.webdriver.remote.webelement.WebElement
            data = row.text.split(" ")

        # clean up
        # replace S. with South
        # replace N. with North
        data = [i.replace('S.', 'South') for i in data]
        data = [i.replace('N.', 'North') for i in data]
        data = [i.replace(',', '') for i in data]
        self.data = [i.replace('+', '') for i in data]

        # if country name is split into 2 elements in the list
        # combine them
        # hopefully no country names split into 3 or more elements
        self.__combine_splited_country_name())

        # convert numerical data into float
        try:
            self.data[1:] = [float(i) for i in self.data[1:]]
        except:
            import pdb; pdb.set_trace()

        # some countries have msising col
        if len(self.data) < 9:
            # replace all entries w/ nan
            country = self.data[0]
            self.data = list(np.zeros(9))
            self.data[0] = country
            self.data[1:] = [np.nan for i in self.data[1:]]

        # put in Pd.Series
        assert len(self.data[:-1]) == 8
        s = pd.Series(self.data[:-1], index=['country', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'active_cases', 'total_recovered', 'serious_critical'])
        return s


    def get_country_from_table(self, country):
        """
        get number for a given country only
        """
        country_element = self.table.find_element_by_xpath("//td[contains(text(), " + country + ")]")   # country
        row = country_element.find_element_by_xpath("./..")
        s = self.get_number_per_row_from_table(row)
        return s


if __name__ == '__main__':
    bot = Coronavirus()
    series = bot.get_country_from_table('China')
    df = bot.get_table_all_country()


