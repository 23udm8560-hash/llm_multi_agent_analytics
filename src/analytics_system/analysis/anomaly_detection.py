import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


def detect_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    numeric = df.select_dtypes(include=np.number)
    result = df.copy()
    result["_is_anomaly"] = False
    if numeric.shape[1] == 0 or len(df) < 10:
        return result
    work = numeric.replace([np.inf, -np.inf], np.nan)
    work = work.fillna(work.median()).fillna(0)
    model = IsolationForest(contamination=min(max(contamination, 0.01), 0.2), random_state=42)
    labels = model.fit_predict(work)
    result["_is_anomaly"] = labels == -1
    return result
