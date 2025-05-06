import os
import pandas as pd
from openad.helpers.paths import parse_path


def col_from_df(df, column_name) -> list:
    """
    Returns a given dataframe's column as a list object.
    """

    if column_name in df:
        return df[column_name].tolist()
    return []


def csv_to_df(cmd_pointer, filename):
    """
    Returns a dataframe from a csv file.
    """

    file_path = parse_path(cmd_pointer, filename)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{filename}' does not exist")
    return pd.read_csv(file_path)
