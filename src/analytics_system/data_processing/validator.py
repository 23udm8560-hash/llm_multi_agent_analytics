import pandas as pd


def validate_csv_filename(name: str) -> bool:
    return str(name).lower().endswith(".csv")


def basic_validation(df: pd.DataFrame) -> list[str]:
    issues = []
    if df.empty:
        issues.append("Dataset has no rows.")
    if df.columns.duplicated().any():
        issues.append("Dataset has duplicate column names.")
    if df.isna().all(axis=None):
        issues.append("Every cell is missing.")
    return issues
