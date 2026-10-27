from analytics_system.agents.visualization_agent import VisualizationAgent


def run_visualization_pipeline(df, chart_type, x, y=None):
    return VisualizationAgent().run(df, chart_type, x, y)
