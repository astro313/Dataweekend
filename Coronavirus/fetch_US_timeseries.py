"""

fetch US data in .csv via Kaggle API

"""

import pandas as pd

def check_ds_in_dir():
    import os
    os.system('ls -l us*.csv')


def pull_ds_from_kaggle():
    import kaggle
    kaggle.api.authenticate()         # based on my credentials in .kaggle/kaggel_json; https://adityashrm21.github.io/Setting-Up-Kaggle/
    kaggle.api.dataset_download_files("sudalairajkumar/covid19-in-usa/", path="./", unzip=True)

    check_ds_in_dir()


if __name__ == '__main__':
    pull_ds_from_kaggle()





