"""

get latest dataset on US via Kaggle, make basic time series plot across US, get NYS and relevant columns and save DF for calculating # of unknown cases.

"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def read_us_ds_csv(fname):
    df = pd.read_csv(fname)
    return df


def convert_dateCol_to_datetime(df):
    df['date'] = pd.to_datetime(df['date'].astype('str'))
    return df


def plot_daily_cases_across_US(df, ylog=False):
    # df1_daily.columns
    """
        date - date of observation
        state - US state 2 digit code
        positive - number of tests with positive results
        negative - number of tests with negative results
        pending - number of test with pending results
        death - number of deaths
        total - total number of tests
    """
    plt.figure()
    plt.plot(df['date'], df['positive'], label='confirmed cases')
    plt.plot(df['date'], df['posNeg'], label='Total tested (excl. pending)')
    plt.plot(df['date'], df['death'], label='Death')

    if ylog:
        plt.yscale('log')

    plt.legend()
    plt.xlabel('Date')
    _ = plt.xticks(rotation=90)

    plt.show(block=False)


def plot_timeseries_by_NYS(df, ylog=False):
    """ numbers are cumulative """

    df = df.loc[df['state'] == 'NY']
    plt.figure()
    plt.plot(df['date'], df['positive'], label='confirmed cases')
    plt.plot(df['date'], df['death'], label='Death')

    if ylog:
        plt.yscale('log')

    plt.legend()
    plt.xlabel('Date')
    _ = plt.xticks(rotation=90)

    plt.show(block=False)
    return df


def create_df_for_realnum_infected(df_state):
    """ Given numbers for a given state, massage data into df to calculate what's real number of infections (both known + unknown) """

    # dataframe updated in place
    df_state['cases'] = df_state['positive']
    df_state['active'] = df_state['positive'] - df_state['death']
    df_state.rename(columns={'death': "deaths"}, inplace=True)
    df_state.sort_values('date', inplace=True)

    df_state.drop('positive', axis=1, inplace=True)
    df_state.drop('pending', axis=1, inplace=True)
    df_state.drop('negative', axis=1, inplace=True)
    df_state.drop('total', axis=1, inplace=True)
    df_state.drop('dateChecked', axis=1, inplace=True)

    df_state.reset_index(inplace=True)
    try:
        df_state.drop('index', axis=1, inplace=True)
    except:
        pass
    df_state.set_index('date', inplace=True)



if __name__ == '__main__':
    # get latest dataset
    from fetch_US_timeseries import pull_ds_from_kaggle
    pull_ds_from_kaggle()

    f1 = 'us_covid19_daily.csv'
    f2 = 'us_states_covid19_daily.csv'
    assert os.path.isfile(f1)
    assert os.path.isfile(f2)
    df1_daily = read_us_ds_csv(fname=f1)
    df2_state = read_us_ds_csv(fname=f2)

    df1_daily = convert_dateCol_to_datetime(df1_daily)
    df2_state = convert_dateCol_to_datetime(df2_state)

    plot_daily_cases_across_US(df1_daily, ylog=True)
    df2_NY = plot_timeseries_by_NYS(df2_state)

    create_df_for_realnum_infected(df2_NY)
    df2_NY.to_pickle('us_NYS_covid19_daily.csv')