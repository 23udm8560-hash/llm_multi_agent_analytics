import pandas as pd
import numpy as np


def correlation_matrix(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include=np.number)
    if numeric.shape[1] < 2:
        return {}
    return numeric.corr(numeric_only=True).round(4).replace({np.nan: None}).to_dict()
