from analytics_system.agents.eda_agent import EDAAgent
from analytics_system.agents.anomaly_detection_agent import AnomalyDetectionAgent


def run_analysis_pipeline(df, detect_anomalies=False):
    result = {"eda": EDAAgent().run(df)}
    if detect_anomalies:
        result["anomalies"] = AnomalyDetectionAgent().run(df)
    return result
