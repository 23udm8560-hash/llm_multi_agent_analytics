import pandas as pd


def parse_datetime_candidates(df: pd.DataFrame) -> pd.DataFrame:
    """Try parsing columns whose names suggest dates; only keep conversion if useful."""
    result = df.copy()
    for col in result.columns:
        if any(token in str(col).lower() for token in ("date", "time", "timestamp")):
            parsed = pd.to_datetime(result[col], errors="coerce")
            if parsed.notna().mean() >= 0.6:
                result[col] = parsed
    return result
