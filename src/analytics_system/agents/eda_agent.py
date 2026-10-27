from analytics_system.analysis.descriptive_stats import descriptive_statistics
from analytics_system.analysis.statistical_tests import correlation_matrix


class EDAAgent:
    name = "EDA Agent"

    def run(self, df):
        return {"descriptive_statistics": descriptive_statistics(df), "correlations": correlation_matrix(df)}
