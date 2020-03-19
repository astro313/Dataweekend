import numpy as np
import matplotlib
import seaborn as sns
# Specify renderer
# matplotlib.use('Agg')

# Boiler-plate settings for producing pub-quality figures
# 1 point = 1/72 inch
from cycler import cycler
matplotlib.rcParams['axes.prop_cycle'] = cycler(color='bgrcmyk')
matplotlib.rcParams.update({'figure.figsize': (8, 5)    # inches
                            , 'font.size': 22      # points
                            , 'legend.fontsize': 16      # points
                            , 'lines.linewidth': 1.5       # points
                            , 'axes.linewidth': 1.5       # points
                            , 'text.usetex': False    # Use LaTeX to layout text
                            , 'font.family': "serif"  # Use serifed fonts
                            , 'xtick.major.size': 10     # length, points
                            , 'xtick.major.width': 1.5     # points
                            , 'xtick.minor.size': 6     # length, points
                            , 'xtick.minor.width': 1     # points
                            , 'ytick.major.size': 10     # length, points
                            , 'ytick.major.width': 1.5     # points
                            , 'ytick.minor.size': 6     # length, points
                            , "xtick.minor.visible": True
                            , "ytick.minor.visible": True
                            , 'font.weight': 'bold'
                            , 'ytick.minor.width': 1     # points
                            , 'font.serif': ("Times", "Palatino", "Computer Modern Roman", "New Century Schoolbook", "Bookman"), 'font.sans-serif': ("Helvetica", "Avant Garde", "Computer Modern Sans serif"), 'font.monospace': ("Courier", "Computer Modern Typewriter"), 'font.cursive': "Zapf Chancery"
                            })


import matplotlib.pyplot as plt
import pandas as pd



def get_germanyTS_from_xlsx(fname="corona_germany_time_series.xlsx")
    # read in Excel file
    xf = pd.ExcelFile(fname)

    df = xf.parse("Sheet1",
        skiprows=0,
        index_col=0,
        names=['dates', 'cases', 'active', 'deaths'])

    # print(df.index)
    return df


if __name__ == '__main__':

    df = get_germanyTS_from_xlsx(fname="corona_germany_time_series.xlsx")
    df =



    import matplotlib.dates as mdates
    plt.close('all')
    # df[['cases', 'active', 'deaths']].plot(figsize=(8, 6))
    fig, ax1 = plt.subplots()
    fig.subplots_adjust(left=0.25, bottom=0.25)
    plt.title('Cumulative')
    plt.plot(df.index, df['cases'].values, label='known cases')
    plt.plot(df.index, df['active'].values, label='active')
    plt.plot(df.index, df['deaths'].values, label='deaths')
    plt.legend()
    monthyearFmt = mdates.DateFormatter('%m-%d')
    ax1.xaxis.set_major_formatter(monthyearFmt)
    _ = plt.xticks(rotation=90)
    plt.ylabel('Number')
    plt.xlabel('Dates')
    plt.show(block=False)


    # death ratio
    closed = df['cases'] - df['active']

    # remove old stuff
    if "healed" in df.columns:
        df.drop('healed', axis=1, inplace=True)

    # calculate
    if "healed" not in df.columns:
        df.insert(loc=len(df.columns),
                  column='healed',
                  value=closed-df['deaths']
            )

    healed_ratio = df['healed']/closed * 100
    death_ratio = df['deaths']/closed * 100

    outcome = {'death_ratio': death_ratio,
                'healed_ratio': healed_ratio}
    outcome_df = pd.DataFrame(outcome)
    outcome_df.plot()
    plt.show(block=False)


    # fit exponential growth
    from scipy.optimize import curve_fit
    def growth_function(x, a, b, c):
        """
        x:
            days since first case

        return:
            function modeling cumulative confirmed cases as exponential growth
        """
        return a * np.exp(b * x ) + c

    def growth(x):
        return growth_function(x, *popt)

    Y = df.cases.values
    X = np.arange(0, len(Y))

    popt, pcov = curve_fit(growth_function, X, Y)

    plt.figure()
    plt.plot(X, Y, 'ko', label='Data')
    plt.plot(X, growth(X), label='Fitted Exp. Growth')
    plt.ylabel('Number of cases')
    plt.xlabel('Days since the first confirmed case')
    plt.legend()
    plt.show(block=False)



    # predictions, using some assumed "known" figures
    days_infected_before_outcome = 14          # account for death rate lages infection rate
    assumed_real_death_rate = 0.7              # percent, s.t. assumed_real_death_rate = # dead / # unknown & known infected * 100; based on seasonal flu

    def create_inverse_growth_func(a, b, c):
        "given cumulated number of cases, return the specific number of days that has passed at that point since first confirmed case"
        inverse = lambda x: np.log((x - c) / a) / b
        return inverse

    # substitute the coefficients from the fit
    inverse_growth = create_inverse_growth_func(*popt)

    # number of cases 'days_infected_before_outcome':
    # assuming we know the death rate (better than percentage of population that'd have it), than we use it to infer the total number of unknown + known cases
    total_cases_days_infection_before = df["deaths"][-1] * 100 / assumed_real_death_rate

    # given number of cases, how many days has it been since the first case exist (cf. detected)
    shift_days = inverse_growth(total_cases_days_infection_before)

    # delays in days in reality
    # Current deaths belong to a total case figure of the past, not to the current case figure in which the outcome (recovery or death) of a proportion (the most recent cases) hasn't yet been determined.
    # The correct formula, therefore, would appear to be:
    # CFR = deaths at day.x / cases at day.x-{T}
    # (where T = average time period from case confirmation to death)
    lackdays = shift_days - len(df) + days_infected_before_outcome
    days_off = lackdays
    print(days_off)

    x = np.arange(0, len(df["cases"]))
    if "real" in df.columns:
        df.drop("real", axis=1, inplace=True)
    df.insert(loc=len(df.columns),
              column="real",
              value=growth(x+days_off).astype(np.int))
    # print(df)


    plt.close('all')
    # df[['cases', 'active', 'deaths']].plot(figsize=(8, 6))
    fig, ax1 = plt.subplots()
    fig.subplots_adjust(left=0.25, bottom=0.25)
    plt.title('Cumulative')
    plt.plot(df.index, df['cases'].values, label='known cases')
    plt.plot(df.index, df['real'].values, label='known + unknown cases')
    plt.legend()
    monthyearFmt = mdates.DateFormatter('%m-%d')
    ax1.xaxis.set_major_formatter(monthyearFmt)
    _ = plt.xticks(rotation=90)
    plt.ylabel('Number')
    plt.xlabel('Dates')
    plt.show(block=False)
