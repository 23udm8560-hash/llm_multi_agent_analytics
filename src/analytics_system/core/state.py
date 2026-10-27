from typing import Any, TypedDict
import pandas as pd


class AnalyticsState(TypedDict, total=False):
    original_df: pd.DataFrame
    cleaned_df: pd.DataFrame
    user_request: str
    profile: dict[str, Any]
    cleaning_report: dict[str, Any]
    eda: dict[str, Any]
    anomalies: pd.DataFrame
    insights: str
    ml_recommendations: dict[str, Any]
    ml_training_results: dict[str, Any]
    selected_agents: list[str]
    errors: list[str]
    status: str
