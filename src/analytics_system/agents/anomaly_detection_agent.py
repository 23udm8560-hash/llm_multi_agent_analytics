from analytics_system.analysis.anomaly_detection import detect_anomalies


class AnomalyDetectionAgent:
    name = "Anomaly Detection Agent"

    def run(self, df, contamination=0.05):
        return detect_anomalies(df, contamination=contamination)
