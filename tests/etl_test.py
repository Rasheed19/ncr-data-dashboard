import pandas as pd
from utils.definitions import Definition


def test_column_existence():

    ncr_data = pd.read_csv(filepath_or_buffer="./data/ncr_data_cleaned.csv")
    difference = pd.Index(Definition.COLUMNS_NEEDED.values()).difference(
        ncr_data.columns
    )

    assert difference.empty is True
