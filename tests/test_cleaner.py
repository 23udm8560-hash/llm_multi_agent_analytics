import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pandas as pd
from analytics_system.data_processing.cleaner import clean_dataframe


def test_clean_dataframe_drops_duplicates_and_fills_missing():
    df = pd.DataFrame({"Sales Amount": [10.0, None, 10.0], "Region Name": ["East", "West", "East"]})
    cleaned, report = clean_dataframe(df)
    assert len(cleaned) == 2
    assert cleaned.isna().sum().sum() == 0
    assert "sales_amount" in cleaned.columns
    assert report["duplicates_removed"] == 1
