import pandas as pd


def validate_dataframe(df: pd.DataFrame) -> None:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("The uploaded CSV has no data rows.")
    if len(df.columns) == 0:
        raise ValueError("The uploaded CSV has no columns.")
    if len(df.columns) > 500:
        raise ValueError("This app limits datasets to 500 columns for safety and usability.")
