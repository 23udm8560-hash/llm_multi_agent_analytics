import pandas as pd


def detect_date_columns(df: pd.DataFrame) -> list[str]:
    found = []
    for col in df.columns:
        if any(t in str(col).lower() for t in ("date", "time", "timestamp")):
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() >= 0.6:
                found.append(str(col))
    return found
