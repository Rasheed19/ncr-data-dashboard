import pandas as pd
import pytest

from utils.definitions import Definition
from utils.processor import get_summary_data


@pytest.fixture
def ncr() -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer="./data/ncr_data_cleaned.csv")


def test_column_existence(ncr):
    difference = pd.Index(Definition.COLUMNS_NEEDED.values()).difference(ncr.columns)

    assert difference.empty


def test_summary_types(ncr):
    summary_data = get_summary_data(ncr)

    assert all(
        [
            isinstance(summary_data.all_day_chargers, int),
            isinstance(summary_data.counties, list),
            isinstance(summary_data.county_with_most_chargers, str),
            isinstance(summary_data.in_service_chargers, int),
            isinstance(summary_data.non_payment_chargers, int),
            isinstance(summary_data.top_ten, dict),
            isinstance(summary_data.total_chargers, int),
        ]
    )
