from analytics_system.visualization.chart_generator import make_chart


class VisualizationAgent:
    name = "Visualization Agent"

    def run(self, df, chart_type, x, y=None):
        return make_chart(df, chart_type, x, y)
