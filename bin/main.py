import pandas as pd

from constants import DATA_PATH
from rpa_challenge import complete_rpa_challenge


def read_input() -> pd.DataFrame:
    """
    Read RPA challenge input spreadsheet

    :return: challenge data
    :rtype: pd.DataFrame
    """
    # Force dtype to str to avoid selenium webdriver typing issues when filling inputs
    input_data = pd.read_excel(DATA_PATH, dtype=str)
    cols = [c.strip() for c in input_data]
    input_data.columns = cols
    return input_data


def main():
    input_data = read_input()
    complete_rpa_challenge(input_data)


if __name__ == '__main__':
    main()
