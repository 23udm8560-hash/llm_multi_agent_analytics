from analytics_system.analysis.statistical_tests import correlation_matrix


class StatisticalAnalysisAgent:
    name = "Statistical Analysis Agent"

    def run(self, df):
        return {"correlations": correlation_matrix(df)}
