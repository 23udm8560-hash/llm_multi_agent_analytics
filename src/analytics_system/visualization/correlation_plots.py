import pandas as pd
import plotly.express as px
import numpy as np


def correlation_heatmap(df: pd.DataFrame):
    numeric = df.select_dtypes(include=np.number)
    if numeric.shape[1] < 2:
        return None
    corr = numeric.corr(numeric_only=True)
    return px.imshow(corr, text_auto=True, aspect="auto", title="Correlation heatmap", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
