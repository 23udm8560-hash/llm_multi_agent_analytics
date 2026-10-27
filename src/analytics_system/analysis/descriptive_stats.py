import pandas as pd
import numpy as np


def descriptive_statistics(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include=np.number)
    summary = {}
    if not numeric.empty:
        summary = numeric.describe().replace({np.nan: None}).to_dict()
    categorical = {}
    for col in df.select_dtypes(exclude=np.number).columns:
        top = df[col].astype("string").value_counts(dropna=False).head(10)
        categorical[str(col)] = {str(k): int(v) for k, v in top.items()}
    return {"numeric_summary": summary, "categorical_top_values": categorical, "rows": int(len(df)), "columns": int(len(df.columns))}
