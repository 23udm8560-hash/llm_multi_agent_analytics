import pandas as pd
import numpy as np


def profile_dataframe(df: pd.DataFrame) -> dict:
    missing = df.isna().sum()
    dtypes = {str(k): str(v) for k, v in df.dtypes.items()}
    numeric = df.select_dtypes(include=np.number)
    categorical = df.select_dtypes(exclude=np.number)
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numeric_columns": [str(c) for c in numeric.columns],
        "categorical_columns": [str(c) for c in categorical.columns],
        "datetime_candidates": [str(c) for c in df.columns if any(t in str(c).lower() for t in ("date", "time", "timestamp"))],
        "missing_total": int(missing.sum()),
        "missing_by_column": {str(k): int(v) for k, v in missing.items() if v > 0},
        "missing_percent_by_column": {str(k): round(float(v / max(len(df), 1) * 100), 2) for k, v in missing.items() if v > 0},
        "duplicate_rows": int(df.duplicated().sum()),
        "dtypes": dtypes,
        "memory_mb": round(float(df.memory_usage(deep=True).sum() / (1024 ** 2)), 2),
    }
