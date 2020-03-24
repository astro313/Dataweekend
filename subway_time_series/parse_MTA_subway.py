import csv
import pandas as pd


def extract_ridership_to_df(fname):

    # useful col from the fname file
    relevantCols = ['UNIT', 'STATION', 'LINENAME', 'DATE', 'TIME', 'ENTRIES']

    # read in chucks of same 'SCP', and keep only the first and the last row, save as dictionary w/ key "date"+"_wkstart" and "date"+"_wkend".
    ridership = {}
    reader = csv.reader(open(fname), delimiter=',')
    header = next(reader)

    ended = 0
    startRow = None
    for row in reader:

        if startRow is None:
            # create a key represented by UNIT, SCP, STATION name, and wkstart or wkend
            this_scp = row[1] + '_' + row[2] + '__' + row[3].replace(' ', '_').replace('/', '_')
            ridership[this_scp + '_wkstart'] = [row[1], row[3], row[4], row[6], row[7], row[9]]
        else:
            # already defined inside while loop
            # use that instead of "row"
            this_scp = startRow[1] + '_' + startRow[2] + '__' + startRow[3].replace(' ', '_').replace('/', '_')
            ridership[this_scp + '_wkstart'] = [startRow[1], startRow[3], startRow[4], startRow[6], startRow[7], startRow[9]]

        bu = []
        while not ended:
            if startRow is None:
                try:
                    nextrow = next(reader)
                except StopIteration:
                    # very last of the file, not more next entry to compare
                    # take the last row as the end
                    ended = 1
            else:
                nextrow = row

            startRow = None
            current_scp = nextrow[1] + '_' + nextrow[2] + '__' + nextrow[3].replace(' ', '_').replace('/', '_')
            if current_scp == this_scp:
                bu.append(nextrow)
            else:
                # reached the last entry of the week for a given turnstile
                if len(bu) == 0:
                    dont_check_wkstart_wkend = True
                    print("only one entry in the file for this turnstile.")
                else:
                    dont_check_wkstart_wkend = False

                ended = 1
                # roll back to 1 previous row before getting back out to the for loop, use this for the next this_scp
                startRow = nextrow

        if not dont_check_wkstart_wkend:
            try:
                ridership[this_scp + '_wkend'] = [bu[-1][1], bu[-1][3], bu[-1][4], bu[-1][6], bu[-1][7], bu[-1][9]]
            except:
                import pdb; pdb.set_trace()

        # just making sure that the UNIT also matches; in other words, the key is unique. Just using SCP itself is not unique, thus also added station name.
        if not dont_check_wkstart_wkend:
            assert ridership[this_scp+"_wkstart"][0] == ridership[this_scp+"_wkend"][0]

            # some registry seem to have issues. The cumulative number of entrance is lower over time...
            # remove those
            if int(ridership[this_scp + '_wkend'][-1]) - int(ridership[this_scp + '_wkstart'][-1]) < 0:
                # print(this_scp)
                # print(ridership[this_scp + '_wkstart'][-1])
                # print(ridership[this_scp + '_wkend'][-1])
                # import pdb; pdb.set_trace()
                ridership.pop(this_scp + '_wkstart')
                ridership.pop(this_scp + '_wkend')

        if dont_check_wkstart_wkend:
            ridership.pop(this_scp + '_wkstart')

        ended = 0
        if len(ridership) % 2:
            import pdb; pdb.set_trace()

    df = pd.DataFrame(ridership)
    df = df.T
    df.columns = relevantCols
    print(df.head(5))
    return df


def get_delta_entrance(df):
    """
    Calculate to total number of entrance in the week covered by the df

    Return
    ------
    total_en: int
        positive number representing the # of entrance at all turnstile in a given week

    """
    en = df['ENTRIES'].astype(int)
    delta_en = en[1::2].values - en[::2].values
    total_en = delta_en.sum()

    # assert that the difference is positive number
    assert total_en > 0
    return total_en


if __name__ == '__main__':
    listofFiles = ['turnstile_200104.txt', 'turnstile_200111.txt', 'turnstile_200125.txt', 'turnstile_200201.txt', 'turnstile_200208.txt', 'turnstile_200215.txt', 'turnstile_200222.txt', 'turnstile_200229.txt', 'turnstile_200307.txt', 'turnstile_200314.txt', 'turnstile_200321.txt']

    total_df = {}
    for fff in listofFiles:
        date = fff[fff.find('_')+3: fff.find('.')]
        # print(date)
        df = extract_ridership_to_df(fff)
        total_df[date] = get_delta_entrance(df)
    # total_df = pd.DataFrame(total_df, columns=['Total_entrance'])

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(total_df)
    plt.show()



